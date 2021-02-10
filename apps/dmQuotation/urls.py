from django.conf.urls import url

from .views import \
    dmQuotationListCreateAPI, \
    dmQuotationRetrieve, \
    dmQuotationItemListCreateAPI, \
    dmQuotationItemRetrieve, \
    dmQuotationCartCreateAPI

urlpatterns = [
    url(r'list/$', dmQuotationListCreateAPI.as_view()),
    url(r'cart/$', dmQuotationCartCreateAPI.as_view()),
    url(r'number/(?P<pk>[0-9]+)$', dmQuotationRetrieve.as_view()),
    url(r'item/$', dmQuotationItemListCreateAPI.as_view()),
    url(r'item/(?P<pk>[0-9]+)$', dmQuotationItemRetrieve.as_view()),
]
