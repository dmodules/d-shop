from decimal import Decimal

from dshop.models import ProductDefault
from dshop.models import ProductVariableVariant

def get_promocodelist_bymodel_bycode(request, model, code):
    try:
        result = [[], 0.00, 0.00]
        if model == "productdefault":
            cproduct = ProductDefault.objects.get(product_code=code)
        if model == "productvariable":
            cproduct = ProductVariableVariant.objects.get(product_code=code)
        for pc in cproduct.get_promocodes(request):
            result[0].append(pc.promocode.name)
            result[1] = Decimal(cproduct.unit_price + 0)
            result[2] = Decimal(cproduct.unit_price - cproduct.get_price(request))
        return result
    except Exception as e:
        print(e)
