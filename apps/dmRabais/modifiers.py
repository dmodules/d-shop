from decimal import Decimal

from django.utils.translation import ugettext_lazy as _

from shop.money import Money
from shop.serializers.cart import ExtraCartRow
from shop.modifiers.base import BaseCartModifier

from .utils import get_discounts_byrequest

from dshop.models import ProductDefault, ProductVariableVariant
from dshop.serializers import ExtraCartRowContent

class DiscountsModifier(BaseCartModifier):
    identifier = "discounts"

    def add_extra_cart_row(self, cart, request):
        results = get_discounts_byrequest(request)
        all_promocodes = ", ".join([str(p) for p in results[0]])
        all_promocodes_code = ", ".join([str(p) for p in results[1]])
        all_prices = Decimal(results[2])
        all_discounts = Decimal(results[3])
        if all_discounts > 0:
            cart.extra_rows["subtotal-before-discounts"] = ExtraCartRow({
                "label": _("Subtotal before discounts"),
                "amount": Money("%0.2f" % all_prices)
            })
            cart.extra_rows[self.identifier] = ExtraCartRow({
                "label": _("Discounts"),
                "amount": Money("%0.2f" % all_discounts)
            })
            if all_promocodes:
                cart.extra_rows["applied-promocodes"] = ExtraCartRowContent({
                    "label": _("Applied promocodes"),
                    "content": all_promocodes,
                    "content_extra": all_promocodes_code
                })

    def add_extra_cart_item_row(self, cart_item, request):
        if type(cart_item.product) == ProductDefault:
            product = ProductDefault.objects.get(product_code=cart_item.product_code)
        else:
            product = ProductVariableVariant.objects.get(product_code=cart_item.product_code)
        if product.get_price(request) != product.unit_price:
            cart_item.extra_rows["price-before-discounts"] = ExtraCartRow({
                "label": _("Price before discounts"),
                "amount": product.unit_price * cart_item.quantity
            })
            cart_item.extra_rows["unit-price-before-discounts"] = ExtraCartRow({
                "label": _("Unit price before discounts"),
                "amount": product.unit_price
            })
        promolist = ", ".join([str(p) + " ("+str(p.promocode.code)+")" for p in product.get_promocodes(request)])
        if promolist:
            cart_item.extra_rows["applied-promocodes"] = ExtraCartRowContent({
                "label": _("Applied promocodes"),
                "content": promolist,
                "content_extra": promolist
            })
