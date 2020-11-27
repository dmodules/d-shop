import re
import json

from django.utils.translation import ugettext_lazy as _, get_language_from_request
from ipware.ip import get_client_ip as get_ip
from django.http import HttpResponse
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.db.models import Q
from django.shortcuts import redirect
from django.shortcuts import render
from easy_thumbnails.files import get_thumbnailer
from django.template.defaultfilters import slugify

from shop.models.defaults.customer import Customer

from boutique.transition import transition_change_notification

from boutique.models import Product

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response as RestResponse

from shop.payment.modifiers import PaymentModifier
from shop.payment.providers import PaymentProvider

from shop.modifiers.pool import cart_modifiers_pool

from shop.models.order import OrderModel
from shop.models.order import OrderPayment
from shop.money import MoneyMaker
from settings import STRIPE_KEY, STRIPE_ACCOUNT_ID, SITE_URL
from .models import StripeOrderData
import stripe

stripe.api_key = STRIPE_KEY
account_id= STRIPE_ACCOUNT_ID

#######################################################################
# ===---   StripePaymentView                                   ---=== #
#######################################################################

def StripeCheckout(request):

  referenceId = request.GET.get('referenceId', None)
  session_id = request.GET.get('session')

  order = OrderModel.objects.get(number=re.sub('\D', '', referenceId))
  order.extra['session_id'] = session_id
  order.save()
  return render(request, 'stripe.html',  {'CHECKOUT_SESSION_ID':session_id})

def StripePaymentCancelView(request):

  return redirect('/commande/')

def StripePaymentView(request):  #Stripe Success View
  print("Stripe Payment View")

  referenceId = request.GET.get('referenceId', None)

  if referenceId is not None:
    order = OrderModel.objects.get(number=re.sub('\D', '', referenceId))
    transactionId = ''
    try:
      Money = MoneyMaker(order.currency)
      amount = Money(order._total)

      order_payment = OrderPayment.objects.create(
                       order=order,
                       amount=amount,
                       transaction_id=transactionId,
                       payment_method='Carte de crédit (Stripe)'
                      )

      try:
          session_id = order.extra['session_id']
          session = stripe.checkout.Session.retrieve(session_id)
          payment_intent_id = session.payment_intent
          payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
          receipt_url = payment_intent.charges.data[0].receipt_url
          
      except Exception as e:
          print(e)

      stripe_data_obj = StripeOrderData.objects.create(order_payment=order_payment,
                                              receipt_url = receipt_url,
                                              stripe_session_data = str(session),
                                              stripe_payment_data =  str(payment_intent))
      order.acknowledge_payment()
      transition_change_notification(order)
      order.save()
      return redirect(order.get_absolute_url())
    except:
      order.cancel_order()
      order.save()
      return redirect('/commande/')
  else:
    return redirect('/commande/')

#######################################################################
# ===---   TestPaymentView                                     ---=== #
#######################################################################

def TestPaymentView(request):
  print("Test Payment View")

  ###########################################
  # THIS IS AN EXAMPLE PAYMENT VIEW
  ###########################################

  ###########################################
  # ===--- MAKE ORDERPAYMENT
  # Here, after a success payment, create Payment
  # You need referenceId and transactionId from payment.py
  # First, get the right order from referenceId
  # >>> order = OrderModel.objects.get(number=re.sub('\D', '', referenceId))
  # Create right amount price with MoneyMaker
  # >>> Money = MoneyMaker(order.currency)
  # >>> amount = Money(order._total)
  # Then create OrderPayment for Order
  # >>> OrderPayment.objects.create(
  # >>>   order=order,
  # >>>   amount=amount,
  # >>>   transaction_id=transactionId,
  # >>>   payment_method='Test (mode développement)'
  # >>> )
  # Make this payment accepted on workflow
  # >>> order.acknowledge_payment()
  # >>> order.save()
  # In the end, redirect user to his order page
  # >>> return redirect(order.get_absolute_url())
  ###########################################
  
  referenceId = request.GET.get('referenceId', None)
  transactionId = request.GET.get('transactionId', None)

  if referenceId is not None and transactionId is not None:
    order = OrderModel.objects.get(number=re.sub('\D', '', referenceId))
    try:
      Money = MoneyMaker(order.currency)
      amount = Money(order._total)
      OrderPayment.objects.create(
        order=order,
        amount=amount,
        transaction_id=transactionId,
        payment_method='Test (mode développement)'
      )
      order.acknowledge_payment()
      order.save()
      return redirect(order.get_absolute_url())
    except:
      order.cancel_order()
      order.save()
      return redirect('/commande/')
  else:
    return redirect('/commande/')

#######################################################################
# ===---   Views used in products                              ---=== #
#######################################################################

class LoadProduits(APIView):
  permission_classes = [AllowAny]

  def get(self, request, *args, **kwargs):
    category = request.GET.get('category', None)
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 2))
    if category is not None:
      category = int(category)
      products = Product.objects.filter(Q(categories=k)|Q(categories__parent=k)|Q(categories__parent__parent=k)|Q(categories__parent__parent__parent=k),active=True).order_by('id')[offset:offset+limit]
      next_products = Product.objects.filter(Q(categories=k)|Q(categories__parent=k)|Q(categories__parent__parent=k)|Q(categories__parent__parent__parent=k),active=True).order_by('id')[offset+limit:offset+limit+limit].count()
    else:
      products = Product.objects.filter(active=True).order_by('id')[offset:offset+limit]
      next_products = Product.objects.filter(active=True).order_by('id')[offset+limit:offset+limit+limit].count()
    # ===---
    all_produits = []
    for produit in products:
      data = {}
      data['name'] = produit.product_name
      data['url'] = produit.get_absolute_url()
      data['price'] = produit.unit_price
      data['caption'] = strip_tags(Truncator(produit.caption).words(18))
      data['slug'] = produit.slug
      if produit.images.first():
        data['image'] = get_thumbnailer(produit.images.first()).get_thumbnail({'size': (510, 510), 'crop': True, 'upscale': True}).url
      else:
        data['image'] = None
      if produit.product_filters.all():
        data['filters'] = " ".join([ slugify(d.name) for d in produit.product_filters.all() ])
      else:
        data['filters'] = None
      all_produits.append(data)
    # ===---
    result = {
      "products": all_produits,
      "next": next_products
    }
    return RestResponse(result)

#######################################################################
# ===---   Views used in frontend                              ---=== #
#######################################################################

class CustomerView(APIView):
  permission_classes = [AllowAny]

  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      customer = {
        "salutation": request.user.customer.salutation,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email
      }
      aso = request.user.customer.shippingaddress_set.first()
      if aso is not None:
        address_shipping = {
          "plugin_order": 1,
          "active_priority": 1,
          "name": aso.name if aso.name is not None else "",
          "address1": aso.address1 if aso.address1 is not None else "",
          "address2": aso.address2 if aso.address2 is not None else "",
          "country": aso.country if aso.country is not None else "",
          "province": aso.province if aso.province is not None else "",
          "city": aso.city if aso.city is not None else "",
          "zip_code": aso.zip_code if aso.zip_code is not None else "",
          "siblings_summary": []
        }
      else:
        address_shipping = {
          "plugin_order": 1,
          "active_priority": "add",
        }
      abo = request.user.customer.billingaddress_set.first()
      if abo is not None:
        address_billing = {
          "plugin_order": 1,
          "active_priority": 1,
          "use_primary_address": False,
          "name": abo.name if abo.name is not None else "",
          "address1": abo.address1 if abo.address1 is not None else "",
          "address2": abo.address2 if abo.address2 is not None else "",
          "country": abo.country if abo.country is not None else "",
          "province": abo.province if abo.province is not None else "",
          "city": abo.city if abo.city is not None else "",
          "zip_code": abo.zip_code if abo.zip_code is not None else "",
          "siblings_summary": []
        }
      else:
        address_billing = {
          "plugin_order": 1,
          "use_primary_address": True
        }
      ###############
      return RestResponse({
        "customer": customer,
        "address_shipping": address_shipping if address_shipping is not None else {},
        "address_billing": address_billing if address_billing is not None else {}
      })
      ###############
    else:
      return RestResponse({"customer": {
          "plugin_order": 1,
          "guest": True
        }, "address_shipping" : {
          "plugin_order": 1,
          "active_priority": "add",
        }
      })

class ShippingMethodsView(APIView):
  permission_classes = [AllowAny]

  def get(self, request, *args, **kwargs):
    result = [m.get_choice() for m in cart_modifiers_pool.get_shipping_modifiers()]
    return RestResponse({"shipping_methods": result})

class BillingMethodsView(APIView):
  permission_classes = [AllowAny]

  def get(self, request, *args, **kwargs):
    result = [m.get_choice() for m in cart_modifiers_pool.get_payment_modifiers()]
    return RestResponse({"billing_methods": result})

def make_stored_request(request):
  return {
    'language': get_language_from_request(request),
    'absolute_base_uri': request.build_absolute_uri('/'),
    'remote_ip': get_ip(request),
    'user_agent': request.META.get('HTTP_USER_AGENT'),
  }