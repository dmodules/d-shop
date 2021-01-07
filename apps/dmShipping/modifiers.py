from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from shop.money import Money
from shop.serializers.cart import ExtraCartRow
from shop.modifiers.pool import cart_modifiers_pool
from shop.shipping.modifiers import ShippingModifier

from django.core.mail import send_mail

from settings import DEFAULT_FROM_EMAIL

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

    def ship_the_goods(self, delivery):

        order_number = delivery.order.number
        shipping_number = delivery.shipping_id
        customer_email = delivery.order.customer.email
        items = []
        for item in delivery.order.items.all():
            data = {
                'name': item.product_name,
                'price': item.unit_price,
                'quantity': item.quantity
            }
            items.append(data)
        try:
            tax = delivery.order.extra['rows'][1][1]
        except Exception as e:
            print(e)
            tax = {}

        try:
            shipping = delivery.order.extra['rows'][2][1]
        except Exception as e:
            print(e)
            shipping = {}

        total_cost = delivery.order.total
        subject = _("Order Number: ") + str(order_number)
        message = ""
        html_message = render_to_string(
            'dshop/shipping/shipping_email.html', {
                'tax': [tax],
                'shipping': [shipping],
                'items': items,
                'order_number': order_number,
                'shipping_number': shipping_number,
                'total_cost': total_cost,
            }
        )

        send_mail(
            subject,
            message,
            DEFAULT_FROM_EMAIL,
            [customer_email],
            html_message=html_message,
            fail_silently=False,
        )

        super().ship_the_goods(delivery)


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
