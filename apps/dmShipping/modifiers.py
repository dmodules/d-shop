from django.utils.translation import ugettext_lazy as _

from shop.money import Money
from shop.serializers.cart import ExtraCartRow
from shop.modifiers.pool import cart_modifiers_pool
from shop.shipping.modifiers import ShippingModifier

from .models import ShippingManagement

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
