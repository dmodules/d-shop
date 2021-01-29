from django.conf.urls import url

from .views import search_product

urlpatterns = [
    url(r'^$', search_product, name='search_product'),
]
