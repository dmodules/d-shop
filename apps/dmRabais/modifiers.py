from decimal import Decimal

from django.utils.translation import ugettext_lazy as _

from shop.money import Money
from shop.serializers.cart import ExtraCartRow
from shop.modifiers.base import BaseCartModifier

from .utils import get_promocodelist_bymodel_bycode

from dshop.models import ProductDefault, ProductVariableVariant

class DiscountsModifier(BaseCartModifier):
    identifier = "discounts"

    def add_extra_cart_row(self, cart, request):
        all_prices = Decimal(0)
        all_discounts = Decimal(0)
        for item in cart.items.all():
            if type(item.product) == ProductDefault:
                model = "productdefault"
            else:
                model = "productvariable"
            results = get_promocodelist_bymodel_bycode(request, model, item.product_code)
            all_prices = all_prices + Decimal(results[1])
            all_discounts = all_discounts + Decimal(results[2])
        if all_discounts > 0:
            cart.extra_rows["subtotal-before-discounts"] = ExtraCartRow({
                "label": _("Subtotal before discounts"),
                "amount": Money("%0.2f" % all_prices)
            })
            cart.extra_rows[self.identifier] = ExtraCartRow({
                "label": _("Discounts"),
                "amount": Money("%0.2f" % all_discounts)
            })

    def add_extra_cart_item_row(self, cart_item, request):
        if type(cart_item.product) == ProductDefault:
            product = ProductDefault.objects.get(product_code=cart_item.product_code)
        else:
            product = ProductVariableVariant.objects.get(product_code=cart_item.product_code)
        if product.get_price(request) != product.unit_price:
            cart_item.extra_rows["price-before-discounts"] = ExtraCartRow({
                "label": _("Price before discounts"),
                "amount": product.unit_price
            })
