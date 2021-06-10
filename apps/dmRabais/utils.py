from decimal import Decimal

from django.db.models import Q

from shop.models.cart import CartModel

from dshop.models import ProductDefault
from dshop.models import ProductVariableVariant

from .models import dmPromoCode


def get_discounts_byrequest(request):
    result = [[], [], Decimal(0), Decimal(0)]
    try:
        cart = CartModel.objects.get_from_request(request)
        for item in cart.items.all():
            if str(item.product.product_model) == "productdefault":
                cproduct = ProductDefault.objects.get(
                    product_code=item.product_code
                )
            if str(item.product.product_model) == "productvariable":
                cproduct = ProductVariableVariant.objects.get(
                    product_code=item.product_code
                )
            for pc in cproduct.get_promocodes(request):
                if hasattr(cart, "subtotal") and pc.promocode.amount:
                    if Decimal(pc.promocode.amount) < Decimal(cart.subtotal):
                        result[0].append(pc.promocode.name)
                        result[1].append(pc.promocode.code)
                else:
                    result[0].append(pc.promocode.name)
                    result[1].append(pc.promocode.code)
            result[2] = result[2] + (Decimal(cproduct.unit_price) * item.quantity) # noqa
            result[3] = result[3] + (
                Decimal(
                    (cproduct.unit_price * item.quantity) - (cproduct.get_price(request) * item.quantity) # noqa
                )
            )
        result[0] = list(dict.fromkeys(result[0]))
        result[1] = list(dict.fromkeys(result[1]))
    except Exception as e:
        print(e)
    return result


def get_cart_discounts(promolist):
    result = [Decimal(0), 0]
    promos = dmPromoCode.objects.filter(
        Q(code__in=promolist),
        is_active=True,
        apply_on_cart=True
    )
    for p in promos:
        if p.amount is not None:
            result[0] = result[0] + Decimal(p.amount)
        elif p.percent is not None:
            result[1] = float(result[1] + p.percent)
    return result
