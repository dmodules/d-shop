from django.utils.translation import ugettext_lazy as _
from django.db import models

from shop.models.order import OrderPayment

#######################################################################
# Stripe
#######################################################################


class StripeOrderData(models.Model):
    order_payment = models.OneToOneField(
        OrderPayment,
        on_delete=models.CASCADE,
        primary_key=True
    )
    receipt_url = models.CharField(
        verbose_name=_("Receipt's URL"),
        max_length=1000
    )
    stripe_session_data = models.TextField(
        verbose_name=_("Stripe's Data")
    )
    stripe_payment_data = models.TextField(
        verbose_name=_("Stripe's Payment Data")
    )

    def __str__(self):
        return str(self.order_payment)
