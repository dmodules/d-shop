import pytz
import json

from decimal import Decimal
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response as RestResponse

from shop.money import Money
from shop.models.customer import CustomerModel

from .models import dmPromoCode
from .models import dmCustomerPromoCode
from .utils import get_promocodelist_bymodel_bycode

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
        if data is not None:
            customer = CustomerModel.objects.get_from_request(request)
            try:
                promocode = dmPromoCode.objects.get(code=data)
                usercodes = dmCustomerPromoCode.objects.filter(
                    customer=customer, promocode=promocode
                )
                if usercodes.count() > 0:
                    return RestResponse({"valid": "already"})
                else:
                    dmCustomerPromoCode.objects.create(
                        customer=customer,
                        promocode=promocode
                    )
                    return RestResponse({"valid": True})
            except Exception as e:
                print(e)
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
        try:
            customer = CustomerModel.objects.get_from_request(request)
            all_promo = dmCustomerPromoCode.objects.filter(
                customer=customer
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
            return RestResponse({"valid": False})

    def post(self, request, *args, **kwargs):
        data = request.GET.get("p", None)
        all_promocodes = []
        all_prices = Decimal(0)
        all_discounts = Decimal(0)
        try:
            datap = json.loads(data)
            for p in datap["products"]:
                pmodel = p["summary"]["product_model"]
                pcode = p["product_code"]
                results = get_promocodelist_bymodel_bycode(request, pmodel, pcode)
                all_promocodes.extend(results[0])
                all_prices = all_prices + Decimal(results[1])
                all_discounts = all_discounts + Decimal(results[2])
        except Exception as e:
            print(e)
            pass
        try:
            customer = CustomerModel.objects.get_from_request(request)
            all_promo = dmCustomerPromoCode.objects.filter(
                customer=customer
            )
            promolist = []
            for p in all_promo:
                today = pytz.utc.localize(datetime.utcnow())
                if p.promocode.valid_until is not None and today > p.promocode.valid_until:
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
                "promolist": promolist,
                "price": Money("%0.2f" % all_prices),
                "discount": Money("%0.2f" % all_discounts)
            })
        except Exception as e:
            print(e)
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
                    return RestResponse({"valid": False})
        else:
            return RestResponse({"valid": False})
