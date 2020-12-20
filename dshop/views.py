import re
import json

from mailchimp3 import MailChimp
from easy_thumbnails.files import get_thumbnailer
from ipware.ip import get_client_ip as get_ip

from django.contrib import messages
from django.utils.translation import ugettext_lazy as _, get_language_from_request
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.core.management import call_command
from django.core.mail import send_mail

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response as RestResponse

from shop.models.defaults.customer import Customer
from shop.payment.modifiers import PaymentModifier
from shop.payment.providers import PaymentProvider
from shop.modifiers.pool import cart_modifiers_pool
from shop.models.order import OrderModel
from shop.models.order import OrderPayment
from shop.money import MoneyMaker

from dshop.transition import transition_change_notification
from dshop.models import Product

from settings import DEFAULT_FROM_EMAIL, DEFAULT_TO_EMAIL
from settings import MAILCHIMP_KEY, MAILCHIMP_LISTID

#######################################################################
# ===---   TestPaymentView                                     ---=== #
#######################################################################


def TestPaymentView(request):
    """
    A development test only view for Payment.
    Will emulate a successfull payment.
    """

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
                payment_method='Test (mode développement)')
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
    """
    Retrieve products.

    GET
    ===

    :param category (int)
    :param offset (int)
    :param limit (int)

    :return An object with the list of Products in "products"
    and the count of Products in the next page in "next".
    """

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        category = request.GET.get('category', None)
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 2))
        if category is not None:
            category = int(category)
            products = Product.objects.filter(
                Q(categories=k) | Q(categories__parent=k)
                | Q(categories__parent__parent=k)
                | Q(categories__parent__parent__parent=k),
                active=True).order_by('id')[offset:offset + limit]
            next_products = Product.objects.filter(
                Q(categories=k) | Q(categories__parent=k)
                | Q(categories__parent__parent=k)
                | Q(categories__parent__parent__parent=k),
                active=True).order_by('id')[offset + limit:offset + limit +
                                            limit].count()
        else:
            products = Product.objects.filter(
                active=True).order_by('id')[offset:offset + limit]
            next_products = Product.objects.filter(
                active=True).order_by('id')[offset + limit:offset + limit +
                                            limit].count()
        # ===---
        all_produits = []
        for produit in products:
            data = {}
            data['name'] = produit.product_name
            data['url'] = produit.get_absolute_url()
            data['caption'] = strip_tags(Truncator(produit.caption).words(18))
            data['slug'] = produit.slug
            if produit.main_image:
                data['image'] = get_thumbnailer(
                    produit.main_image).get_thumbnail({
                        'size': (540, 600),
                        'crop': True,
                        'upscale': True
                    }).url
            elif produit.images.first():
                data['image'] = get_thumbnailer(
                    produit.images.first()).get_thumbnail({
                        'size': (540, 600),
                        'crop': True,
                        'upscale': True
                    }).url
            else:
                data['image'] = None
            if produit.filters.all():
                data['filters'] = " ".join(
                    [slugify(d.name) for d in produit.filters.all()])
            else:
                data['filters'] = None
            if hasattr(produit, 'variants'):
                data['variants'] = True
                data['price'] = produit.variants.first().unit_price
            else:
                data['price'] = produit.get_price(request)
                data['realprice'] = produit.unit_price
                data['variants'] = False
            all_produits.append(data)
        # ===---
        result = {"products": all_produits, "next": next_products}
        return RestResponse(result)


#######################################################################
# ===---   Views used in frontend                              ---=== #
#######################################################################


class CustomerView(APIView):
    """
    Retrieve current customer data
    to be used in the frontend app.

    GET
    ===

    Check if a customer is authenticated.

    Check if customer's shipping address exist.

    Check if customer's billing address exist.

    :return An object with customer basic informations,
    customer's shipping address and customer's billing address.
    """

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
                    "address1":
                    aso.address1 if aso.address1 is not None else "",
                    "address2":
                    aso.address2 if aso.address2 is not None else "",
                    "country": aso.country if aso.country is not None else "",
                    "province":
                    aso.province if aso.province is not None else "",
                    "city": aso.city if aso.city is not None else "",
                    "zip_code":
                    aso.zip_code if aso.zip_code is not None else "",
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
                    "address1":
                    abo.address1 if abo.address1 is not None else "",
                    "address2":
                    abo.address2 if abo.address2 is not None else "",
                    "country": abo.country if abo.country is not None else "",
                    "province":
                    abo.province if abo.province is not None else "",
                    "city": abo.city if abo.city is not None else "",
                    "zip_code":
                    abo.zip_code if abo.zip_code is not None else "",
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
                "address_shipping":
                address_shipping if address_shipping is not None else {},
                "address_billing":
                address_billing if address_billing is not None else {}
            })
            ###############
        else:
            return RestResponse({
                "customer": {
                    "plugin_order": 1,
                    "guest": True
                },
                "address_shipping": {
                    "plugin_order": 1,
                    "active_priority": "add",
                },
                "address_billing": {
                    "plugin_order": 1,
                    "use_primary_address": True,
                }
            })


class ShippingMethodsView(APIView):
    """
    Retrieve all shipping methods
    to be used in the frontend app.

    GET
    ===

    :return An object with all shipping methods.
    """

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        result = [
            m.get_choice()
            for m in cart_modifiers_pool.get_shipping_modifiers()
        ]
        return RestResponse({"shipping_methods": result})


class BillingMethodsView(APIView):
    """
    Retrieve all billing methods
    to be used in the frontend app.

    GET
    ===

    :return An object with all billing methods.
    """

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        result = [
            m.get_choice()
            for m in cart_modifiers_pool.get_payment_modifiers()
        ]
        return RestResponse({"billing_methods": result})


def make_stored_request(request):
    """
    Create some data from request and
    return an object to be stored in some shop's models
    """

    return {
        'language': get_language_from_request(request),
        'absolute_base_uri': request.build_absolute_uri('/'),
        'remote_ip': get_ip(request),
        'user_agent': request.META.get('HTTP_USER_AGENT'),
    }


def mailchimp(request):
    """
    Evaluate a "calcul" answer.
    If okay, create a member in the client's mailchimp list.

    MAILCHIMP_KEY in settings.py

    MAILCHIMP_LISTID in settings.py
    """

    client = MailChimp(mc_api=MAILCHIMP_KEY)
    email = request.POST.get('email_infolettre', '')
    calcul = request.POST.get('calcul_infolettre', '')
    if calcul == '6':
        try:
            client.lists.members.create(MAILCHIMP_LISTID, {
                'email_address': email,
                'status': 'subscribed',
            })
            messages.success(
                request,
                'Vous avez bien été ajouté à notre liste de courriels')
        except:
            messages.error(request,
                           'Oups, il y a un problème avec votre inscription')
            redirect('/')
    else:
        messages.error(request, 'La réponse du calcul est mauvaise')
    return redirect('/')


def sendemail(request):
    """
    Retrieve form data and send an email
    to the client.
    Then, redirect to the page /message-envoye/.

    DEFAULT_FROM_EMAIL in settings.py

    DEFAULT_TO_EMAIL in settings.py
    """

    send_mail(
        'Message du formulaire de contact de votre site web',
        'Bonjour, voici le message:\n\nNom: ' + request.POST.get('name') +
        '\nCourriel: ' + request.POST.get('email') + '\nTéléphone: ' +
        request.POST.get('phone') + '\nSujet: ' + request.POST.get('subject') +
        '\nMessage:\n' + request.POST.get('message'),
        DEFAULT_FROM_EMAIL,
        [DEFAULT_TO_EMAIL],
        fail_silently=False,
    )
    call_command('send_queued_mail')
    return redirect('/message-envoye/')
