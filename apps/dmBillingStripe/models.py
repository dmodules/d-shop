from django.utils.translation import ugettext_lazy as _
from django.db import models

from shop.models.order import OrderPayment

#######################################################################
# Stripe
#######################################################################


class StripeOrderData(models.Model):
    order_payment = models.OneToOneField(OrderPayment,
                                         on_delete=models.CASCADE,
                                         primary_key=True)
    receipt_url = models.CharField(verbose_name=_("URL de réception"),
                                   max_length=150)
    stripe_session_data = models.TextField(verbose_name=_("Stripe données"))
    stripe_payment_data = models.TextField(
        verbose_name=_("Stripe de la facture"))

    def __str__(self):
        return str(self.order_payment)
