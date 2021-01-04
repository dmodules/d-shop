from dshop.models import ProductDefault
from dshop.models import ProductVariableVariant

def get_promocodelist_bymodel_bycode(request, model, code):
    try:
        result = []
        if model == "productdefault":
            cproduct = ProductDefault.objects.get(product_code=code)
        if model == "productvariable":
            cproduct = ProductVariableVariant.objects.get(product_code=code)
        for pc in cproduct.get_promocodes(request):
            result.append(pc.promocode.name)
        return result
    except Exception as e:
        print(e)
