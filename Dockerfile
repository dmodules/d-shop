# <WARNING>
# Everything within sections like <TAG> is generated and can
# be automatically replaced on deployment. You can disable
# this functionality by simply removing the wrapping tags.
# </WARNING>

# <DOCKER_FROM>
FROM divio/base:4.18-py3.6-slim-stretch
# </DOCKER_FROM>

# BEGIN: installing and building frontend	
ENV NODE_VERSION=12.16.1 NPM_VERSION=6.14.9	
COPY node.sh /app/	
RUN bash /app/node.sh	

ENV NODE_PATH=$NVM_DIR/versions/node/v$NODE_VERSION/lib/node_modules \	
    PATH=$NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH	

ENV PATH=/app/frontend/node_modules/.bin:$PATH	
COPY /frontend/ /app/frontend/	
RUN (cd /app/frontend/ && npm install && npm run build && rm -rf /tmp/*)	
# END: installing and building frontend

# <PYTHON>
ENV PIP_INDEX_URL=${PIP_INDEX_URL:-https://wheels.aldryn.net/v1/aldryn-extras+pypi/${WHEELS_PLATFORM:-aldryn-baseproject-py3}/+simple/} \
    WHEELSPROXY_URL=${WHEELSPROXY_URL:-https://wheels.aldryn.net/v1/aldryn-extras+pypi/${WHEELS_PLATFORM:-aldryn-baseproject-py3}/}
COPY requirements.* /app/
COPY addons-dev /app/addons-dev/
RUN pip-reqs compile && \
    pip-reqs resolve && \
    pip install \
        --no-index --no-deps \
        --requirement requirements.urls
# </PYTHON>

# <SOURCE>
COPY . /app
# </SOURCE>

# <STATIC>
RUN DJANGO_MODE=build python manage.py collectstatic --noinput
# </STATIC>
