import re
import stripe

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.shortcuts import render
from django.db import transaction

from settings import STRIPE_SECRET_KEY

from shop.money import MoneyMaker
from shop.models.order import OrderModel
from shop.models.order import OrderPayment

from dshop.transition import transition_change_notification
from dshop.models import Product, ProductDefault

from .models import StripeOrderData

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
    if referenceId is not None:
        order = OrderModel.objects.get(number=re.sub(r"\D", "", referenceId))
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
            except Exception as e:
                print("Error to update quantity")
                #!TODO
    return redirect("/")

def StripePaymentView(request):
    referenceId = request.GET.get("referenceId", None)
    if referenceId is not None:
        order = OrderModel.objects.get(number=re.sub(r"\D", "", referenceId))
        transactionId = ""
        try:
            Money = MoneyMaker(order.currency)
            amount = Money(order._total)
            order_payment = OrderPayment.objects.create(
                order=order,
                amount=amount,
                transaction_id=transactionId,
                payment_method=_("Carte de crédit (Stripe)"))
            try:
                session_id = order.extra["session_id"]
                session = stripe.checkout.Session.retrieve(session_id)
                payment_intent_id = session.payment_intent
                payment_intent = stripe.PaymentIntent.retrieve(
                    payment_intent_id)
                receipt_url = payment_intent.charges.data[0].receipt_url
            except Exception as e:
                print(e)
            StripeOrderData.objects.create(
                order_payment=order_payment,
                receipt_url=receipt_url,
                stripe_session_data=str(session),
                stripe_payment_data=str(payment_intent))
            order.acknowledge_payment()
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
            order.save()
            return redirect(order.get_absolute_url())
        except Exception as e:
            print(e)
            order.save()
            return redirect("/vos-commandes/")
    else:
        return redirect("/vos-commandes/")
