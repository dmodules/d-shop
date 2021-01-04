from django.utils.translation import ugettext_lazy as _

from shop.money import Money
from shop.serializers.cart import ExtraCartRow
from shop.modifiers.pool import cart_modifiers_pool
from shop.shipping.modifiers import ShippingModifier

from .models import ShippingManagement


class FreeShippingModifier(ShippingModifier):
    identifier = "free-shipping"

    def get_choice(self):
        sm = ShippingManagement.objects.filter(
            identifier=self.identifier).first()
        if sm:
            return (self.identifier, sm.name)
        return (None, None)

    def add_extra_cart_row(self, cart, request):
        # ===---
        shipping_modifiers = cart_modifiers_pool.get_shipping_modifiers()
        if not self.is_active(
            cart.extra.get("shipping_modifier")
        ) and len(shipping_modifiers) > 1:
            return
        # ===---
        sm = ShippingManagement.objects.filter(
            identifier=self.identifier).first()
        if sm:
            amount = Money("0")
            instance = {"label": _("Shipping costs"), "amount": amount}
            cart.extra_rows[self.identifier] = ExtraCartRow(instance)
            cart.total += amount


class StandardShippingModifier(ShippingModifier):
    identifier = "standard-shipping"

    def get_choice(self):
        sm = ShippingManagement.objects.filter(
            identifier=self.identifier).first()
        if sm:
            return (self.identifier, sm.name)
        return (None, None)

    def add_extra_cart_row(self, cart, request):
        # ===---
        shipping_modifiers = cart_modifiers_pool.get_shipping_modifiers()
        if not self.is_active(
            cart.extra.get("shipping_modifier")
        ) and len(shipping_modifiers) > 1:
            return
        # ===---
        sm = ShippingManagement.objects.filter(
            identifier=self.identifier).first()
        cp = float(str(cart.subtotal).split(" ")[1].replace(",", "."))
        if sm:
            if (sm.use_separator and sm.separator is not None
                    and sm.price_after is not None and cp >= sm.separator):
                amount = Money(sm.price_after)
            else:
                amount = Money(sm.price)
            instance = {"label": _("Shipping costs"), "amount": amount}
            cart.extra_rows[self.identifier] = ExtraCartRow(instance)
            cart.total += amount


class ExpressShippingModifier(ShippingModifier):
    identifier = "express-shipping"

    def get_choice(self):
        sm = ShippingManagement.objects.filter(
            identifier=self.identifier).first()
        if sm:
            return (self.identifier, sm.name)
        return (None, None)

    def add_extra_cart_row(self, cart, request):
        # ===---
        shipping_modifiers = cart_modifiers_pool.get_shipping_modifiers()
        if not self.is_active(cart.extra.get(
                "shipping_modifier")) and len(shipping_modifiers) > 1:
            return
        # ===---
        sm = ShippingManagement.objects.filter(
            identifier=self.identifier).first()
        cp = float(str(cart.subtotal).split(" ")[1].replace(",", "."))
        if sm:
            if (sm.use_separator and sm.separator is not None
                    and sm.price_after is not None and cp >= sm.separator):
                amount = Money(sm.price_after)
            else:
                amount = Money(sm.price)
            instance = {"label": _("Shipping costs"), "amount": amount}
            cart.extra_rows[self.identifier] = ExtraCartRow(instance)
            cart.total += amount


class StandardShippingWithSeparatorModifier(ShippingModifier):
    identifier = "standard-separator-shipping"

    def get_choice(self):
        sm = ShippingManagement.objects.filter(
            identifier=self.identifier).first()
        if sm:
            return (self.identifier, sm.name)
        return (None, None)

    def add_extra_cart_row(self, cart, request):
        # ===---
        shipping_modifiers = cart_modifiers_pool.get_shipping_modifiers()
        if not self.is_active(cart.extra.get(
                "shipping_modifier")) and len(shipping_modifiers) > 1:
            return
        # ===---
        sm = ShippingManagement.objects.filter(
            identifier=self.identifier).first()
        cp = float(str(cart.subtotal).split(" ")[1].replace(",", "."))
        if sm:
            if (sm.use_separator and sm.separator is not None
                    and sm.price_after is not None and cp >= sm.separator):
                amount = Money(sm.price_after)
            else:
                amount = Money(sm.price)
            instance = {"label": _("Shipping costs"), "amount": amount}
            cart.extra_rows[self.identifier] = ExtraCartRow(instance)
            cart.total += amount


class ExpressShippingWithSeparatorModifier(ShippingModifier):
    identifier = "express-separator-shipping"

    def get_choice(self):
        sm = ShippingManagement.objects.filter(
            identifier=self.identifier).first()
        if sm:
            return (self.identifier, sm.name)
        return (None, None)

    def add_extra_cart_row(self, cart, request):
        # ===---
        shipping_modifiers = cart_modifiers_pool.get_shipping_modifiers()
        if not self.is_active(cart.extra.get(
                "shipping_modifier")) and len(shipping_modifiers) > 1:
            return
        # ===---
        sm = ShippingManagement.objects.filter(
            identifier=self.identifier).first()
        cp = float(str(cart.subtotal).split(" ")[1].replace(",", "."))
        if sm:
            if (sm.use_separator and sm.separator is not None
                    and sm.price_after is not None and cp >= sm.separator):
                amount = Money(sm.price_after)
            else:
                amount = Money(sm.price)
            instance = {"label": _("Shipping costs"), "amount": amount}
            cart.extra_rows[self.identifier] = ExtraCartRow(instance)
            cart.total += amount
