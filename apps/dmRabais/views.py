import pytz
import json

from decimal import Decimal
from datetime import datetime

from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response as RestResponse

from shop.money import Money
from shop.models.customer import CustomerModel
from shop.models.defaults.order import Order

from dshop.models import \
    ProductDefault, \
    ProductVariable, \
    ProductVariableVariant

from .models import dmPromoCode
from .models import dmCustomerPromoCode
from .utils import get_discounts_byrequest, get_cart_discounts

#######################################################################
# ===---   Views used in frontend                              ---=== #
#######################################################################


class PromoCodesCreate(APIView):
    """
    Retrieve current customer data
    to be used in the frontend app.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):  # noqa: C901
        data = request.GET.get("promocode", None)
        products = request.GET.get("p", None)
        if data is not None:
            customer = CustomerModel.objects.get_from_request(request)
            try:
                promocode = dmPromoCode.objects.get(code=data)
                if promocode.customer.all():
                    if customer not in promocode.customer.all():
                        return RestResponse({"valid": False})

                usercodes = dmCustomerPromoCode.objects.filter(
                    customer=customer,
                    promocode=promocode
                )
                # Check date validation
                today = pytz.utc.localize(datetime.utcnow())
                if promocode.valid_until is not None and today > promocode.valid_until: # noqa
                    promocode.is_active = False
                    promocode.save()
                elif today < promocode.valid_from:
                    return RestResponse({"valid": False})
                if not promocode.is_active:
                    return RestResponse({"valid": "expired"})
                elif usercodes.count() > 0 and not usercodes[0].promocode.allow_multiple: # noqa
                    return RestResponse({"valid": "already"})
                elif usercodes.count() > 0 and \
                  usercodes[0].promocode.allow_multiple and \ # noqa
                  usercodes[0].promocode.customer.all().count() > 0 and \ # noqa
                  customer not in usercodes[0].promocode.customer.all(): # noqa
                    return RestResponse({"valid": "already"})
                else:
                    if usercodes.count() > 0 and \
                       usercodes[0].promocode.allow_multiple and \
                       (
                           usercodes[0].promocode.customer.all().count() == 0 or # noqa
                           usercodes[0].promocode.customer.all().count() > 0 and # noqa
                           customer in usercodes[0].promocode.customer.all()
                       ):
                        usercodes[0].delete()
                    cpromo = dmCustomerPromoCode.objects.create(
                        customer=customer,
                        promocode=promocode
                    )
                    # Check uses validation
                    if promocode.valid_uses > 0:
                        howmanyuses = dmCustomerPromoCode.objects.filter(
                            promocode=promocode
                        ).count()
                        if howmanyuses > promocode.valid_uses:
                            promocode.is_active = False
                            promocode.save()
                            cpromo.delete()
                            return RestResponse({"valid": "expired"})
                    # Check order validation
                    if products is not None:
                        results = get_discounts_byrequest(request)
                        if cpromo.promocode.name in results[0]:
                            return RestResponse({"valid": True})
                        else:
                            cpromo.delete()
                            return RestResponse({"valid": "inapplicable"})
                    else:
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

    def get(self, request, *args, **kwargs):  # noqa: C901
        try:
            customer = CustomerModel.objects.get_from_request(request)
            # get all promocodes
            all_promo = dmCustomerPromoCode.objects.filter(
                customer=customer
            )
            # get all used promocodes
            customer_orders = Order.objects.filter(
                ~Q(status="new"),
                ~Q(status="created"),
                customer=customer
            )
            used_promolist = []
            for o in customer_orders:
                try:
                    for row in o.extra["rows"]:
                        if "applied-promocodes" in row:
                            if row[1]["content_extra"]:
                                for c in row[1]["content_extra"].split(", "):
                                    if c not in used_promolist:
                                        used_promolist.append(c)
                except Exception:
                    pass
            # make promocodes list
            promolist = []
            for p in all_promo:
                # expire if date passed
                today = pytz.utc.localize(datetime.utcnow())
                if p.promocode.valid_until is not None and \
                   today > p.promocode.valid_until:
                    p.is_expired = True
                    p.save()
                # expire if already used
                if p.promocode.code in used_promolist:
                    # un-expire promocode if multiple_allowed and all/selected customer # noqa
                    if p.promocode.allow_multiple and \
                       (
                           p.promocode.customer.all().count() == 0 or
                           customer in p.promocode.customer.all()
                       ):
                        p.is_expired = p.is_expired
                        p.save()
                    else:
                        p.is_expired = True
                        p.save()
                # add to list
                datas = {}
                datas["name"] = p.promocode.name
                datas["is_expired"] = p.is_expired
                datas["on_discounted"] = p.promocode.can_apply_on_discounted
                promolist.append(datas)
            ###############
            return RestResponse({
                "valid": True,
                "promolist": promolist
            })
        except Exception as e:
            print(e)
            return RestResponse({"valid": False})

    def post(self, request, *args, **kwargs):  # noqa: C901
        all_promocodes = []
        all_prices = Decimal(0)
        all_discounts = Decimal(0)
        try:
            customer = CustomerModel.objects.get_from_request(request)
            # get all promocodes
            all_promo = dmCustomerPromoCode.objects.filter(
                customer=customer
            )
            # get all actually usable promocodes and discounts
            results = get_discounts_byrequest(request)
            all_promocodes = results[0]
            all_prices = Decimal(results[2])
            all_discounts = Decimal(results[3])
            # ===---
            sub = Money(0)
            for item in customer.cart.items.all():
                if type(item.product) == ProductDefault:
                    sub += item.quantity * item.product.get_price(request)
                elif type(item.product) == ProductVariable:
                    sub += item.quantity * ProductVariableVariant.objects.get(
                        product_code=item.product_code
                    ).get_price(request)
            # ===---
            if len(results[1]) > 0:
                cart_discounts = get_cart_discounts(results[1])
                if cart_discounts[1] > 0:
                    percent_discount = Decimal(
                        float(sub) * (cart_discounts[1] / 100)
                    )
                else:
                    percent_discount = Money(0)
                all_discounts = all_discounts + cart_discounts[0] + Decimal(percent_discount) # noqa
            if all_discounts < 0:
                all_discounts = 0
            # get all used promocodes
            customer_orders = Order.objects.filter(
                ~Q(status="new"),
                ~Q(status="created"),
                customer=customer
            )
            used_promolist = []
            for o in customer_orders:
                try:
                    for row in o.extra["rows"]:
                        if "applied-promocodes" in row:
                            if row[1]["content_extra"]:
                                for c in row[1]["content_extra"].split(", "):
                                    if c not in used_promolist:
                                        used_promolist.append(c)
                except Exception:
                    pass
            # make promocodes list
            promolist = []
            for p in all_promo:
                # expire if date passed
                today = pytz.utc.localize(datetime.utcnow())
                if p.promocode.valid_until is not None and \
                   today > p.promocode.valid_until:
                    p.is_expired = True
                    p.save()
                # expire if already used
                if p.promocode.code in used_promolist:
                    # un-expire promocode if multiple_allowed and all/selected customer  # noqa
                    if p.promocode.allow_multiple and \
                       (
                           p.promocode.customer.all().count() == 0 or
                           customer in p.promocode.customer.all()
                       ):
                        p.is_expired = p.is_expired
                        p.save()
                    else:
                        p.is_expired = True
                        p.save()
                # add to list
                datas = {}
                if p.promocode.name in all_promocodes:
                    datas["name"] = p.promocode.name
                    datas["is_expired"] = p.is_expired
                    datas["on_discounted"] = p.promocode.can_apply_on_discounted # noqa
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
                            cpc = dmCustomerPromoCode.objects.get(
                                customer=request.user.customer,
                                promocode__name=p
                            )
                            cpc.is_expired = True
                            cpc.save()
                    return RestResponse({"valid": True})
                except Exception as e:
                    print(e)
                    return RestResponse({"valid": False})
        else:
            return RestResponse({"valid": False})
