from django.conf.urls import url

from .views import StripePaymentView, StripeCheckout, StripePaymentCancelView

urlpatterns = [
    url(r'^checkout/$', StripeCheckout),
    url(r'^payment/$', StripePaymentView),
    url(r'^cancel/$', StripePaymentCancelView)
]
