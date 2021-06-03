FROM python:3.6

WORKDIR /app
COPY . /app

# BEGIN: installing and building frontend	

RUN apt-get update -y
RUN apt-get install curl gnupg -y \
gettext
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash
RUN apt-get install nodejs -y

WORKDIR /app/frontend
RUN npm install
WORKDIR /app/frontend/src
RUN npm run build

# END: installing and building frontend

WORKDIR /app

RUN pip install -r requirements.txt
#RUN python manage.py collectstatic --noinput

CMD uwsgi --http=0.0.0.0:80 --module=wsgi