from django.conf.urls import url

from .views import get_data

urlpatterns = [
    url(r'^get-data/', get_data),
]
