from django.utils.translation import ugettext_lazy as _
from decimal import Decimal

from shop.serializers.cart import ExtraCartRow
from shop.payment.modifiers import PaymentModifier

from .payment import StripePayment

#######################################################################
# ===---   Payments: Stripe                                    ---=== #
#######################################################################

class StripePaymentModifier(PaymentModifier):
  payment_provider = StripePayment()
  commision_percentage = None

  def get_choice(self):
    return (self.identifier, _("Carte de crédit"))

  def is_disabled(self, cart):
    return cart.total == 0

  def add_extra_cart_row(self, cart, request):
    if not self.is_active(cart) or not self.commision_percentage:
      return
    amount = cart.total * Decimal(self.commision_percentage / 100.0)
    instance = {'label': _("+ {}% handling fee").format(self.commision_percentage), 'amount': amount}
    cart.extra_rows[self.identifier] = ExtraCartRow(instance)
    cart.total += amount

  def update_render_context(self, context):
    super().update_render_context(context)
    context['payment_modifiers']['stripe_payment'] = True
