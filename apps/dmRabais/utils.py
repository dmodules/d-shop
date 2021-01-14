from decimal import Decimal

from shop.models.cart import CartModel

from dshop.models import ProductDefault
from dshop.models import ProductVariableVariant

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
                result[0].append(pc.promocode.name)
                result[1].append(pc.promocode.code)
            result[2] = result[2] + (Decimal(cproduct.unit_price) * item.quantity)
            result[3] = result[3] + (
                Decimal(
                    (cproduct.unit_price * item.quantity) - (cproduct.get_price(request) * item.quantity)
                )
            )
        result[0] = list(dict.fromkeys(result[0]))
        result[1] = list(dict.fromkeys(result[1]))
    except Exception as e:
        print(e)
    return result
