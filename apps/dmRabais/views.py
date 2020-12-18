import pytz
import json
from datetime import datetime

from django.utils.translation import ugettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response as RestResponse

from dshop.models import ProductDefault
from dshop.models import ProductVariableVariant

from .models import dmPromoCode
from .models import dmCustomerPromoCode

#######################################################################
# ===---   Views used in frontend                              ---=== #
#######################################################################


class PromoCodesCreate(APIView):
    """
    Retrieve current customer data
    to be used in the frontend app.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.GET.get("promocode", None)
        print(data)
        if request.user.is_authenticated:
            if data is not None:
                try:
                    promocode = dmPromoCode.objects.get(code=data)
                    usercodes = dmCustomerPromoCode.objects.filter(
                        customer=request.user.customer,
                        promocode=promocode
                    )
                    if usercodes.count() > 0:
                        return RestResponse({"valid": "already"})
                    else:
                        dmCustomerPromoCode.objects.create(
                            customer=request.user.customer,
                            promocode=promocode
                        )
                        return RestResponse({"valid": True})
                except Exception:
                    return RestResponse({"valid": False})
            else:
                return RestResponse({"valid": False})
        else:
            return RestResponse({"valid": False})


class PromoCodesList(APIView):
    """
    Retrieve current customer data
    to be used in the frontend app.
    """

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                all_promo = dmCustomerPromoCode.objects.filter(
                    customer=request.user.customer
                )
                promolist = []
                for p in all_promo:
                    if p.promocode.valid_until is not None:
                        today = pytz.utc.localize(datetime.utcnow())
                        if today > p.promocode.valid_until:
                            p.is_expired = True
                            p.save()
                    datas = {}
                    datas["name"] = p.promocode.name
                    datas["is_expired"] = p.is_expired
                    promolist.append(datas)
                ###############
                return RestResponse({
                    "valid": True,
                    "promolist": promolist
                })
            except Exception as e:
                print(e)
                return RestResponse({
                    "valid": False
                })
        else:
            return RestResponse({"valid": False})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data = request.GET.get("p", None)
            all_promocodes = []
            if data is not None:
                datap = json.loads(data)
                if "products" in datap:
                    for p in datap["products"]:
                        pmodel = p["summary"]["product_model"]
                        pcode = p["product_code"]
                        if pmodel == "productdefault":
                            cproduct = ProductDefault.objects.get(
                                product_code=pcode
                            )
                            for pc in cproduct.get_promocodes(request):
                                all_promocodes.append(pc.promocode.name)
                        if pmodel == "productvariable":
                            cproduct = ProductVariableVariant.objects.get(
                                product_code=pcode
                            )
                            for pc in cproduct.get_promocodes(request):
                                all_promocodes.append(pc.promocode.name)
            try:
                all_promo = dmCustomerPromoCode.objects.filter(
                    customer=request.user.customer
                )
                promolist = []
                for p in all_promo:
                    if p.promocode.valid_until is not None:
                        today = pytz.utc.localize(datetime.utcnow())
                        if today > p.promocode.valid_until:
                            p.is_expired = True
                            p.save()
                    datas = {}
                    if p.promocode.name in all_promocodes:
                        datas["name"] = p.promocode.name
                        datas["is_expired"] = p.is_expired
                        promolist.append(datas)
                ###############
                return RestResponse({
                    "valid": True,
                    "promolist": promolist
                })
            except Exception as e:
                print(e)
                return RestResponse({
                    "valid": False
                })
        else:
            return RestResponse({"valid": False})


class PromoCodesOff(APIView):
    """
    Set to is_expired true used promocodes
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data = request.GET.get("p", None)
            if data is not None:
                try:
                    datap = json.loads(data)
                    if "products" in datap:
                        for p in datap["products"]:
                            cpc = None
                            try:
                                cpc = dmCustomerPromoCode.objects.get(
                                    customer=request.user.customer,
                                    promocode__name=p
                                )
                                cpc.is_expired = True
                                cpc.save()
                            except Exception as e:
                                print(e)
                    return RestResponse({"valid": True})
                except Exception as e:
                    print(e)
                    return RestResponse({
                        "valid": False
                    })
        else:
            return RestResponse({"valid": False})
