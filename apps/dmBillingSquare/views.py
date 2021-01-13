import re

from django.shortcuts import redirect

from shop.money import MoneyMaker
from shop.models.order import OrderModel
from shop.models.order import OrderPayment

from dshop.transition import transition_change_notification

try:
    from apps.dmRabais.models import dmCustomerPromoCode
except ImportError:
    dmCustomerPromoCode = None


#######################################################################
# ===---   Square                                              ---=== #
#######################################################################


def SquarePaymentView(request):  # noqa: C901
    """
    Create Order Payment inside Order then aknowlegde payment
    """

    checkoutId = request.GET.get("checkoutId", None)
    referenceId = request.GET.get("referenceId", None)
    transactionId = request.GET.get("transactionId", None)
    if checkoutId is not None and referenceId is not None and transactionId is not None:
        oid = re.sub(r"\D", "", referenceId)
        order = OrderModel.objects.get(number=oid)
        try:
            Money = MoneyMaker(order.currency)
            amount = Money(order._total)
            OrderPayment.objects.create(
                order=order,
                amount=amount,
                transaction_id=transactionId,
                payment_method="Square"
            )
            order.acknowledge_payment()
            order.save()
            # ===---
            try:
                if dmCustomerPromoCode is not None:
                    for extra in order.extra["rows"]:
                        if "applied-promocodes" in extra:
                            promo = extra[1]["content_extra"].split(", ")
                            for pm in promo:
                                cpc = dmCustomerPromoCode.objects.get(
                                    customer=request.user.customer,
                                    promocode__code=pm
                                )
                                cpc.is_expired = True
                                cpc.save()
            except Exception as e:
                print(e)
            # ===---
            try:
                items = []
                for i in order.items.all():
                    datas = {}
                    datas["quantity"] = i.quantity
                    datas["summary"] = {}
                    datas["summary"]["product_name"] = str(i)
                    datas["line_total"] = i.line_total
                    items.append(datas)
                miniorder = {
                    "number": str(referenceId),
                    "url": "/vos-commandes/"+str(referenceId)+"/"+str(order.token),
                    "items": items,
                    "extra": order.extra,
                    "total": order.total
                }
                transition_change_notification(
                    order,
                    miniorder
                )
            except Exception as e:
                print("When : transition_change_notification")
                print(e)
            # ===---
            return redirect(order.get_absolute_url())
        except Exception as e:
            print(e)
            order.save()
            return redirect("/vos-commandes/")
    else:
        return redirect("/vos-commandes/")
