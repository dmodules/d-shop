from django.conf.urls import url

from .views import SquarePaymentView

urlpatterns = [
    url(r'^payment/$', SquarePaymentView),
]
