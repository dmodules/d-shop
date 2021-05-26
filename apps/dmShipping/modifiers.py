from django.utils.translation import ugettext_lazy as _

from shop.money import Money
from shop.serializers.cart import ExtraCartRow
from shop.modifiers.pool import cart_modifiers_pool
from shop.shipping.modifiers import ShippingModifier

from dshop.transition import transition_change_notification
from .models import ShippingManagement
from .utils import get_price


class PickupShippingModifier(ShippingModifier):
    identifier = "pickup-in-store"

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
            try:
                if cart.shipping_address:
                    price = get_price(
                        self.identifier,
                        cart.shipping_address.country,
                        cart.shipping_address.province,
                        cart.shipping_address.city
                    )
                    amount = Money(price)
            except Exception as e:
                print(str(e) + " : Error while getting shipping price")
            if (sm.use_separator and sm.separator is not None
                    and sm.price_after is not None and cp >= sm.separator):
                amount = Money(sm.price_after)
            instance = {"label": _("Shipping costs"), "amount": amount}
            instance = {"label": _("Shipping costs"), "amount": amount}
            cart.extra_rows[self.identifier] = ExtraCartRow(instance)
            cart.total += amount


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

    def ship_the_goods(self, delivery):
        order_number = delivery.order.number
        shipping_number = delivery.shipping_id
        # ===---
        try:
            items = []
            for i in delivery.order.items.all():
                datas = {}
                datas["quantity"] = i.quantity
                datas["summary"] = {}
                datas["summary"]["product_name"] = str(i)
                datas["line_total"] = i.line_total
                datas["extra"] = i.extra
                items.append(datas)
            miniorder = {
                "status": delivery.order.status,
                "number": str(order_number),
                "url": "/vos-commandes/"+str(order_number)+"/"+str(delivery.order.token),
                "items": items,
                "extra": delivery.order.extra,
                "subtotal": delivery.order.subtotal,
                "total": delivery.order.total,
                "billing_address_text": delivery.order.billing_address_text,
                "shipping_address_text": delivery.order.shipping_address_text,
                "delivery": {
                    "method": delivery.shipping_method,
                    "shipping_id": shipping_number
                }
            }
            transition_change_notification(
                delivery.order,
                miniorder
            )
        except Exception as e:
            print("When : transition_change_notification")
            print(e)
        # ===---
        super().ship_the_goods(delivery)


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
            try:
                if cart.shipping_address:
                    price = get_price(
                        self.identifier,
                        cart.shipping_address.country,
                        cart.shipping_address.province,
                        cart.shipping_address.city
                    )
                    amount = Money(price)
            except Exception as e:
                print(str(e) + " : Error while getting shipping price")
            if (sm.use_separator and sm.separator is not None
                    and sm.price_after is not None and cp >= sm.separator):
                amount = Money(sm.price_after)
            instance = {"label": _("Shipping costs"), "amount": amount}
            instance = {"label": _("Shipping costs"), "amount": amount}
            cart.extra_rows[self.identifier] = ExtraCartRow(instance)
            cart.total += amount

    def ship_the_goods(self, delivery):
        order_number = delivery.order.number
        shipping_number = delivery.shipping_id
        # ===---
        try:
            items = []
            for i in delivery.order.items.all():
                datas = {}
                datas["quantity"] = i.quantity
                datas["summary"] = {}
                datas["summary"]["product_name"] = str(i)
                datas["line_total"] = i.line_total
                datas["extra"] = i.extra
                items.append(datas)
            miniorder = {
                "status": delivery.order.status,
                "number": str(order_number),
                "url": "/vos-commandes/"+str(order_number)+"/"+str(delivery.order.token),
                "items": items,
                "extra": delivery.order.extra,
                "subtotal": delivery.order.subtotal,
                "total": delivery.order.total,
                "billing_address_text": delivery.order.billing_address_text,
                "shipping_address_text": delivery.order.shipping_address_text,
                "delivery": {
                    "method": delivery.shipping_method,
                    "shipping_id": shipping_number
                }
            }
            transition_change_notification(
                delivery.order,
                miniorder
            )
        except Exception as e:
            print("When : transition_change_notification")
            print(e)
        # ===---
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
            try:
                if cart.shipping_address:
                    price = get_price(
                        self.identifier,
                        cart.shipping_address.country,
                        cart.shipping_address.province,
                        cart.shipping_address.city
                    )
                    amount = Money(price)
            except Exception as e:
                print(str(e) + " : Error while getting shipping price")
            if (sm.use_separator and sm.separator is not None
                    and sm.price_after is not None and cp >= sm.separator):
                amount = Money(sm.price_after)
            instance = {"label": _("Shipping costs"), "amount": amount}
            instance = {"label": _("Shipping costs"), "amount": amount}
            cart.extra_rows[self.identifier] = ExtraCartRow(instance)
            cart.total += amount

    def ship_the_goods(self, delivery):
        order_number = delivery.order.number
        shipping_number = delivery.shipping_id
        # ===---
        try:
            items = []
            for i in delivery.order.items.all():
                datas = {}
                datas["quantity"] = i.quantity
                datas["summary"] = {}
                datas["summary"]["product_name"] = str(i)
                datas["line_total"] = i.line_total
                datas["extra"] = i.extra
                items.append(datas)
            miniorder = {
                "status": delivery.order.status,
                "number": str(order_number),
                "url": "/vos-commandes/"+str(order_number)+"/"+str(delivery.order.token),
                "items": items,
                "extra": delivery.order.extra,
                "subtotal": delivery.order.subtotal,
                "total": delivery.order.total,
                "billing_address_text": delivery.order.billing_address_text,
                "shipping_address_text": delivery.order.shipping_address_text,
                "delivery": {
                    "method": delivery.shipping_method,
                    "shipping_id": shipping_number
                }
            }
            transition_change_notification(
                delivery.order,
                miniorder
            )
        except Exception as e:
            print("When : transition_change_notification")
            print(e)
        # ===---
        super().ship_the_goods(delivery)


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
            try:
                if cart.shipping_address:
                    price = get_price(
                        self.identifier,
                        cart.shipping_address.country,
                        cart.shipping_address.province,
                        cart.shipping_address.city
                    )
                    amount = Money(price)
            except Exception as e:
                print(str(e) + " : Error while getting shipping price")
            if (sm.use_separator and sm.separator is not None
                    and sm.price_after is not None and cp >= sm.separator):
                amount = Money(sm.price_after)
            instance = {"label": _("Shipping costs"), "amount": amount}
            instance = {"label": _("Shipping costs"), "amount": amount}
            cart.extra_rows[self.identifier] = ExtraCartRow(instance)
            cart.total += amount

    def ship_the_goods(self, delivery):
        order_number = delivery.order.number
        shipping_number = delivery.shipping_id
        # ===---
        try:
            items = []
            for i in delivery.order.items.all():
                datas = {}
                datas["quantity"] = i.quantity
                datas["summary"] = {}
                datas["summary"]["product_name"] = str(i)
                datas["line_total"] = i.line_total
                datas["extra"] = i.extra
                items.append(datas)
            miniorder = {
                "status": delivery.order.status,
                "number": str(order_number),
                "url": "/vos-commandes/"+str(order_number)+"/"+str(delivery.order.token),
                "items": items,
                "extra": delivery.order.extra,
                "subtotal": delivery.order.subtotal,
                "total": delivery.order.total,
                "billing_address_text": delivery.order.billing_address_text,
                "shipping_address_text": delivery.order.shipping_address_text,
                "delivery": {
                    "method": delivery.shipping_method,
                    "shipping_id": shipping_number
                }
            }
            transition_change_notification(
                delivery.order,
                miniorder
            )
        except Exception as e:
            print("When : transition_change_notification")
            print(e)
        # ===---
        super().ship_the_goods(delivery)


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
            try:
                if cart.shipping_address:
                    price = get_price(
                        self.identifier,
                        cart.shipping_address.country,
                        cart.shipping_address.province,
                        cart.shipping_address.city
                    )
                    amount = Money(price)
            except Exception as e:
                print(str(e) + " : Error while getting shipping price")
            if (sm.use_separator and sm.separator is not None
                    and sm.price_after is not None and cp >= sm.separator):
                amount = Money(sm.price_after)
            instance = {"label": _("Shipping costs"), "amount": amount}
            instance = {"label": _("Shipping costs"), "amount": amount}
            cart.extra_rows[self.identifier] = ExtraCartRow(instance)
            cart.total += amount

    def ship_the_goods(self, delivery):
        order_number = delivery.order.number
        shipping_number = delivery.shipping_id
        # ===---
        try:
            items = []
            for i in delivery.order.items.all():
                datas = {}
                datas["quantity"] = i.quantity
                datas["summary"] = {}
                datas["summary"]["product_name"] = str(i)
                datas["line_total"] = i.line_total
                datas["extra"] = i.extra
                items.append(datas)
            miniorder = {
                "status": delivery.order.status,
                "number": str(order_number),
                "url": "/vos-commandes/"+str(order_number)+"/"+str(delivery.order.token),
                "items": items,
                "extra": delivery.order.extra,
                "subtotal": delivery.order.subtotal,
                "total": delivery.order.total,
                "billing_address_text": delivery.order.billing_address_text,
                "shipping_address_text": delivery.order.shipping_address_text,
                "delivery": {
                    "method": delivery.shipping_method,
                    "shipping_id": shipping_number
                }
            }
            transition_change_notification(
                delivery.order,
                miniorder
            )
        except Exception as e:
            print("When : transition_change_notification")
            print(e)
        # ===---
        super().ship_the_goods(delivery)
