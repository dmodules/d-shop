from django.conf.urls import url

from .views import PromoCodesCreate, PromoCodesList, PromoCodesOff

urlpatterns = [
    url(r'^promocode/$', PromoCodesCreate.as_view()),
    url(r'^promocodes/$', PromoCodesList.as_view()),
    url(r'^promocodesoff/$', PromoCodesOff.as_view())
]
