from django.utils.translation import ugettext_lazy as _

from decimal import Decimal

from shop.serializers.cart import ExtraCartRow
from shop.modifiers.defaults import DefaultCartModifier
from shop.payment.modifiers import PaymentModifier

from .models import ProductVariable

# AJOUTER LES PROPRIÉTÉS DES VARIANTES DANS "VARIABLES" DE "EXTRA"


class PrimaryCartModifier(DefaultCartModifier):
    def process_cart_item(self, cart_item, request):
        variant = cart_item.product.get_product_variant(
            product_code=cart_item.product_code
        )
        cart_item.unit_price = variant.get_price(request)
        cart_item.line_total = cart_item.unit_price * cart_item.quantity
        cart_item.extra["variables"] = {"code": cart_item.product_code}
        if type(cart_item.product) == ProductVariable:
            pv = cart_item.product.variants.get(
                product_code=cart_item.product_code
            )
            attributes = []
            for a in pv.attribute.all():
                attributes.append(str(a))
            cart_item.extra["variables"]["attributes"] = attributes
        return super(
            DefaultCartModifier, self
        ).process_cart_item(cart_item, request)
