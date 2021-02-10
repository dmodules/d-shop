from django.conf.urls import url

from .views import \
    dmQuotationListCreateAPI, \
    dmQuotationRetrieve, \
    dmQuotationItemListCreateAPI, \
    dmQuotationItemRetrieve

urlpatterns = [
    url(r'$', dmQuotationListCreateAPI.as_view()),
    url(r'(?P<pk>[0-9]+)$', dmQuotationRetrieve.as_view()),
    url(r'item/$', dmQuotationItemListCreateAPI.as_view()),
    url(r'item/(?P<pk>[0-9]+)$', dmQuotationItemRetrieve.as_view()),
]
