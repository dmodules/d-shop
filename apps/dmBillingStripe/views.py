import re
import stripe

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse
from django.template import loader
from django.conf import settings

from settings import STRIPE_SECRET_KEY, SQUARE_SYNC

from shop.money import MoneyMaker
from shop.models.order import OrderModel
from shop.models.order import OrderPayment

from dshop.transition import transition_change_notification
from dshop.models import ProductDefault

from apps.dmSquare.views import square_update_stock
from .models import StripeOrderData

try:
    from apps.dmRabais.models import dmCustomerPromoCode
except ImportError:
    dmCustomerPromoCode = None

stripe.api_key = STRIPE_SECRET_KEY

#######################################################################
# ===---   Stripe                                              ---=== #
#######################################################################


def StripeCheckout(request):
    referenceId = request.GET.get("referenceId", None)
    session_id = request.GET.get("session")
    order = OrderModel.objects.get(number=re.sub(r"\D", "", referenceId))
    order.extra["session_id"] = session_id
    order.save()
    return render(request, "stripe.html", {"CHECKOUT_SESSION_ID": session_id})


def StripePaymentCancelView(request):
    referenceId = request.GET.get("referenceId", None)
    error_code = request.GET.get("error_code", None)
    error_message = request.GET.get("error_message", None)
    couponID = request.GET.get("cp", None)
    if referenceId is not None:
        order = OrderModel.objects.get(number=re.sub(r"\D", "", referenceId))
        if couponID is not None:
            stripe.Coupon.delete(couponID)
        if 'cancel' not in order.extra:
            cart = order.customer.cart
            order.readd_to_cart(cart)
            try:
                with transaction.atomic():
                    for item in cart.items.all():
                        db_product = item.product
                        if type(db_product) == ProductDefault:
                            db_product.quantity += item.quantity
                            db_product.save()
                        else:
                            p_code = item.product_code
                            pv = db_product.variants.get(product_code=p_code)
                            pv.quantity += item.quantity
                            pv.save()
                # Param to identify order is canceled
                order.extra['cancel'] = '1'
                order.save()
            except Exception as e:
                print("Error while cancelling Stripe Payment.")
                print(e)
                # !TODO

    template = loader.get_template(
        "theme/{}/pages/payment_error.html".format(settings.THEME_SLUG)
    )
    context = {
        'error_code': error_code,
        'error_message': error_message
    }
    return HttpResponse(template.render(context, request))


def StripePaymentView(request):  # noqa: C901
    referenceId = request.GET.get("referenceId", None)
    charge_id = request.GET.get("charge", None)
    couponID = request.GET.get("cp", None)
    if referenceId is not None:
        order = OrderModel.objects.get(number=re.sub(r"\D", "", referenceId))
        transactionId = charge_id
        try:
            Money = MoneyMaker(order.currency)
            amount = Money(order._total)
            order_payment = OrderPayment.objects.create(
                order=order,
                amount=amount,
                transaction_id=transactionId,
                payment_method=_("Credit Card (via Stripe)")
            )
            try:
                charge = stripe.Charge.retrieve(charge_id)
                receipt_url = charge.receipt_url
            except Exception as e:
                print(e)
            StripeOrderData.objects.create(
                order_payment=order_payment,
                receipt_url=receipt_url,
                # stripe_session_data=str(session),
                stripe_payment_data=str(charge))
            order.acknowledge_payment()
            # ===---
            # Update quantity in Square
            if SQUARE_SYNC == "1":
                try:
                    for item in order.items.all():
                        product_code = item.product_code
                        quantity = item.quantity
                        square_update_stock(quantity, product_code)
                except Exception as e:
                    print(e)
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
            if couponID is not None:
                stripe.Coupon.delete(couponID)
            # ===---
            # We want to skip few steps.
            # So add delivery creation on payment success.
            try:
                items = []
                for i in order.items.all():
                    data = {}
                    data["deliver_quantity"] = i.quantity
                    data["id"] = i
                    data["canceled"] = i.canceled
                    items.append(data)
                order.update_or_create_delivery(items)
            except Exception as e:
                print("Error to create delivery: " + str(e))
            # ===---
            order.save()
            # ===---
            try:
                items = []
                for i in order.items.all():
                    datas = {}
                    datas["quantity"] = i.quantity
                    datas["summary"] = {}
                    name = str(i.product.product_name_trans)
                    datas["summary"]["product_name"] = name
                    datas["line_total"] = i.line_total
                    datas["extra"] = i.extra
                    items.append(datas)
                url = "/vos-commandes/"+str(referenceId)+"/"+str(order.token)
                miniorder = {
                    "number": str(referenceId),
                    "url": url,
                    "items": items,
                    "extra": order.extra,
                    "subtotal": order.subtotal,
                    "total": order.total,
                    "billing_address_text": order.billing_address_text,
                    "shipping_address_text": order.shipping_address_text
                }
                transition_change_notification(
                    order,
                    miniorder
                )
            except Exception as e:
                print("When : transition_change_notification")
                print(e)
            return redirect(order.get_absolute_url())
        except Exception as e:
            print(e)
            order.save()
            return redirect("/vos-commandes/")
    else:
        return redirect("/vos-commandes/")
