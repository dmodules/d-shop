import re
import stripe

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.shortcuts import render

from settings import STRIPE_KEY, SITE_URL

from shop.money import MoneyMaker
from shop.models.order import OrderModel
from shop.models.order import OrderPayment
from shop.models.defaults.customer import Customer

from boutique.transition import transition_change_notification

from .models import StripeOrderData

stripe.api_key = STRIPE_KEY

#######################################################################
# ===---   Stripe                                              ---=== #
#######################################################################

def StripeCheckout(request):
  referenceId = request.GET.get("referenceId", None)
  session_id = request.GET.get("session")
  order = OrderModel.objects.get(number = re.sub("\D", "", referenceId))
  order.extra["session_id"] = session_id
  order.save()
  return render(request, "stripe.html",  {"CHECKOUT_SESSION_ID": session_id})

def StripePaymentCancelView(request):
  return redirect("/commande/")

def StripePaymentView(request):
  referenceId = request.GET.get("referenceId", None)
  if referenceId is not None:
    order = OrderModel.objects.get(number=re.sub("\D", "", referenceId))
    transactionId = ""
    try:
      Money = MoneyMaker(order.currency)
      amount = Money(order._total)
      order_payment = OrderPayment.objects.create(
        order = order,
        amount = amount,
        transaction_id = transactionId,
        payment_method = _("Carte de crédit (Stripe)")
      )
      try:
        session_id = order.extra["session_id"]
        session = stripe.checkout.Session.retrieve(session_id)
        payment_intent_id = session.payment_intent
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        receipt_url = payment_intent.charges.data[0].receipt_url
      except Exception as e:
        print(e)
      StripeOrderData.objects.create(
        order_payment = order_payment,
        receipt_url = receipt_url,
        stripe_session_data = str(session),
        stripe_payment_data =  str(payment_intent)
      )
      order.acknowledge_payment()
      transition_change_notification(order)
      order.save()
      return redirect(order.get_absolute_url())
    except:
      order.cancel_order()
      order.save()
      return redirect("/commande/")
  else:
    return redirect("/commande/")
