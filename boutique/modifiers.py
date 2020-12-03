from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from shop.modifiers.pool import cart_modifiers_pool
from shop.modifiers.defaults import DefaultCartModifier
from shop.serializers.cart import ExtraCartRow
from shop.money import Money
from shop.shipping.modifiers import ShippingModifier
from shop.payment.modifiers import PaymentModifier

from .payment import TestPayment
from .payment import StripePayment
from .payment import SquarePayment
from decimal import Decimal

from shop.conf import app_settings
from shop.modifiers.base import BaseCartModifier
from boutique.models import CanadaTaxManagement, ShippingAddress
from boutique.models import ShippingManagement

class PrimaryCartModifier(DefaultCartModifier):
  def process_cart_item(self, cart_item, request):
    variant = cart_item.product.get_product_variant(product_code=cart_item.product_code)
    cart_item.unit_price = variant.get_price(request)
    cart_item.line_total = cart_item.unit_price * cart_item.quantity
    cart_item.extra["variables"] = {
      _("Code du produit"): cart_item.product_code
    }
    return super(DefaultCartModifier, self).process_cart_item(cart_item, request)

class FreeShippingModifier(ShippingModifier):
  identifier = 'free-shipping'

  def get_choice(self):
    shippingMethods = ShippingManagement.objects.all()
    for sm in shippingMethods:
      if sm.identifier == self.identifier:
        return (self.identifier, sm.name)
    return (None, None)

  def add_extra_cart_row(self, cart, request):
    shipping_modifiers = cart_modifiers_pool.get_shipping_modifiers()
    if not self.is_active(cart.extra.get('shipping_modifier')) and len(shipping_modifiers) > 1:
      return

    shippingMethods = ShippingManagement.objects.all()
    for sm in shippingMethods:
      if sm.identifier == self.identifier:
        amount = Money('0')
        instance = {'label': _("Shipping costs"), 'amount': amount}
        cart.extra_rows[self.identifier] = ExtraCartRow(instance)
        cart.total += amount

class StandardShippingModifier(ShippingModifier):
  identifier = 'standard-shipping'

  def get_choice(self):
    shippingMethods = ShippingManagement.objects.all()
    for sm in shippingMethods:
      if sm.identifier == self.identifier:
        return (self.identifier, sm.name)
    return (None, None)

  def add_extra_cart_row(self, cart, request):
    shipping_modifiers = cart_modifiers_pool.get_shipping_modifiers()
    if not self.is_active(cart.extra.get('shipping_modifier')) and len(shipping_modifiers) > 1:
      return

    shippingMethods = ShippingManagement.objects.all()
    for sm in shippingMethods:
      if sm.identifier == self.identifier:
        amount = Money(sm.price)
        instance = {'label': _("Shipping costs"), 'amount': amount}
        cart.extra_rows[self.identifier] = ExtraCartRow(instance)
        cart.total += amount

class ExpressShippingModifier(ShippingModifier):
  identifier = 'express-shipping'

  def get_choice(self):
    shippingMethods = ShippingManagement.objects.all()
    for sm in shippingMethods:
      if sm.identifier == self.identifier:
        return (self.identifier, sm.name)
    return (None, None)

  def add_extra_cart_row(self, cart, request):
    shipping_modifiers = cart_modifiers_pool.get_shipping_modifiers()
    if not self.is_active(cart.extra.get('shipping_modifier')) and len(shipping_modifiers) > 1:
      return

    shippingMethods = ShippingManagement.objects.all()
    for sm in shippingMethods:
      if sm.identifier == self.identifier:
        amount = Money(sm.price)
        instance = {'label': _("Shipping costs"), 'amount': amount}
        cart.extra_rows[self.identifier] = ExtraCartRow(instance)
        cart.total += amount

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
    instance = {'label': _("+ {}% handling fee").format(self.commision_percentage), 'amount': amount}
    cart.extra_rows[self.identifier] = ExtraCartRow(instance)
    cart.total += amount

  def update_render_context(self, context):
    super().update_render_context(context)
    context['payment_modifiers']['test_payment'] = True

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

#######################################################################
# ===---   Payments: Square                                    ---=== #
#######################################################################

class SquarePaymentModifier(PaymentModifier):
  payment_provider = SquarePayment()
  commision_percentage = None

  def get_choice(self):
    return (self.identifier, _("Square (carte de crédit)"))

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
    context['payment_modifiers']['square_payment'] = True

#######################################################################
# ===---   Taxes: Canada                                       ---=== #
#######################################################################

class CanadaTaxModifier(BaseCartModifier):
  identifier = 'canadiantaxes'
  taxes = 1 - 1 / (1 + app_settings.VALUE_ADDED_TAX / 100)

  def add_extra_cart_row(self, cart, request):
    amount = cart.subtotal * self.taxes
    instance = {
      'label': _("{}% VAT incl.").format(app_settings.VALUE_ADDED_TAX),
      'amount': amount,
    }
    try:
      shippingaddress = ShippingAddress.objects.filter(customer=request.customer).first()
      if shippingaddress:
        if shippingaddress.country == 'CA':
          state = shippingaddress.province
          if state == "Colombie-Britannique":
            state = "British Columbia"
          elif state == "Nouveau-Brunswick":
            state = "New-Brunswick"
          elif state == "Terre-Neuve et Labrador":
            state = "Newfoundland and Labrador"
          elif state == "Territoires du Nord-Ouest":
            state = "Northwest Territories"
          elif state == "Nouvelle-Écosse":
            state = "Nova Scotia"
          elif state == "Île-du-Prince-Édouard":
            state = "Prince Edward Island"
          elif state == "Québec":
            state = "Quebec"
          tax = CanadaTaxManagement.objects.get(state=state)
          hst = tax.hst if tax.hst else Decimal('0')
          gst = tax.gst if tax.gst else Decimal('0')
          pst = tax.pst if tax.pst else Decimal('0')
          qst = tax.qst if tax.qst else Decimal('0')
          tax = (hst + gst + pst + qst)
          amount = cart.subtotal * tax / 100
          instance = {
            'label': _("{}% TOTAL incl.").format(tax),
            'amount': amount,
          }
    except:
      pass
    try:
      if hst != Decimal('0'):
        data1 = {
          'label': _("{}% HST incl.").format(hst),
          'amount': cart.subtotal * hst / 100,
        }
        cart.extra_rows['data1'] = ExtraCartRow(data1)
      if gst != Decimal('0'):
        data2 = {
          'label': _("{}% GST incl.").format(gst),
          'amount': cart.subtotal * gst / 100,
        }
        cart.extra_rows['data2'] = ExtraCartRow(data2)
      if pst != Decimal('0'):
        data3 = {
          'label': _("{}% PST incl.").format(pst),
          'amount': cart.subtotal * pst / 100,
        }
        cart.extra_rows['data3'] = ExtraCartRow(data3)
      if qst != Decimal('0'):
        data4 = {
          'label': _("{}% QST incl.").format(qst),
          'amount': cart.subtotal * qst / 100,
        }
        cart.extra_rows['data4'] = ExtraCartRow(data4)
    except:
        pass
    cart.extra_rows[self.identifier] = ExtraCartRow(instance)
    cart.total += amount
