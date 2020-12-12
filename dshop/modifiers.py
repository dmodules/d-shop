from django.utils.translation import ugettext_lazy as _

from decimal import Decimal

from shop.money import Money
from shop.serializers.cart import ExtraCartRow
from shop.modifiers.defaults import DefaultCartModifier
from shop.payment.modifiers import PaymentModifier

from .payment import TestPayment

# AJOUTER LES PROPRIÉTÉS DES VARIANTES DANS "VARIABLES" DE "EXTRA"

class PrimaryCartModifier(DefaultCartModifier):
  def process_cart_item(self, cart_item, request):
    variant = cart_item.product.get_product_variant(product_code=cart_item.product_code)
    cart_item.unit_price = variant.get_price(request)
    cart_item.line_total = cart_item.unit_price * cart_item.quantity
    cart_item.extra["variables"] = {
      "code": cart_item.product_code
    }
    return super(DefaultCartModifier, self).process_cart_item(cart_item, request)

#######################################################################
# ===---   Payments: Test                                      ---=== #
#######################################################################

class TestPaymentModifier(PaymentModifier):
  payment_provider = TestPayment()
  commision_percentage = None

  def get_choice(self):
    return (self.identifier, _("Test (mode développement)"))

  def is_disabled(self, cart):
    return cart.total == 0

  def add_extra_cart_row(self, cart, request):
    if not self.is_active(cart) or not self.commision_percentage:
      return
    amount = cart.total * Decimal(self.commision_percentage / 100.0)
    instance = {
      "label": _("+ {}% handling fee").format(self.commision_percentage),
      "amount": amount
    }
    cart.extra_rows[self.identifier] = ExtraCartRow(instance)
    cart.total += amount

  def update_render_context(self, context):
    super().update_render_context(context)
    context["payment_modifiers"]["test_payment"] = True
