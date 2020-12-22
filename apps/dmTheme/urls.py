from django.conf.urls import url

from .views import get_css

urlpatterns = [
    url(r'^get-css/$', get_css),
]
