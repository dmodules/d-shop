import re
import json

from mailchimp3 import MailChimp
from easy_thumbnails.files import get_thumbnailer
from ipware.ip import get_client_ip as get_ip

from cms.models import Title

from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language_from_request
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.shortcuts import redirect
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import slugify
from django.core.management import call_command
from django.core.mail import send_mail

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response as RestResponse
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.views import APIView
from rest_framework import status

from shop.money import Money
from shop.models.defaults.customer import Customer
from shop.modifiers.pool import cart_modifiers_pool
from shop.models.order import OrderModel
from shop.models.order import OrderPayment
from shop.money import MoneyMaker
from shop.rest.renderers import CMSPageRenderer
from shop.serializers.auth import PasswordResetConfirmSerializer

from dshop.models import Product
from dshop.models import AttributeValue
from dshop.transition import transition_change_notification

from settings import DEFAULT_FROM_EMAIL, DEFAULT_TO_EMAIL
from settings import MAILCHIMP_KEY, MAILCHIMP_LISTID
from feature_settings import *

try:
    from apps.dmRabais.models import dmCustomerPromoCode
except ImportError:
    dmCustomerPromoCode = None


#######################################################################
# ===---   TestPaymentView                                     ---=== #
#######################################################################


def TestPaymentView(request):
    """
    A development test only view for Payment.
    Will emulate a successfull payment.
    """

    print("Test Payment View")

    referenceId = request.GET.get("referenceId", None)
    transactionId = request.GET.get("transactionId", None)

    if referenceId is not None and transactionId is not None:
        order = OrderModel.objects.get(number=re.sub(r"\D", "", referenceId))
        try:
            Money = MoneyMaker(order.currency)
            amount = Money(order._total)
            OrderPayment.objects.create(
                order=order,
                amount=amount,
                transaction_id=transactionId,
                payment_method="Test (development)"
            )
            order.acknowledge_payment()
            order.save()
            # ===---
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
            # ===---
            try:
                items = []
                for i in order.items.all():
                    datas = {}
                    datas["quantity"] = i.quantity
                    datas["summary"] = {}
                    datas["summary"]["product_name"] = str(i)
                    datas["line_total"] = i.line_total
                    datas["extra"] = i.extra
                    items.append(datas)
                miniorder = {
                    "number": str(referenceId),
                    "url": "/vos-commandes/"+str(referenceId)+"/"+str(order.token),
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
            # ===---
            return redirect(order.get_absolute_url())
        except Exception as e:
            print(e)
            order.save()
            return redirect("/vos-commandes/")
    else:
        return redirect("/vos-commandes/")


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
        category = request.GET.get("category", None)
        brand = request.GET.get("brand", None)
        offset = int(request.GET.get("offset", 0))
        limit = int(request.GET.get("limit", 2))
        if category is not None:
            category = int(category)
            products = Product.objects.filter(
                Q(categories=category) | Q(categories__parent=category)
                | Q(categories__parent__parent=category)
                | Q(categories__parent__parent__parent=category),
                active=True).distinct()[offset:offset + limit]
            next_products = Product.objects.filter(
                Q(categories=category) | Q(categories__parent=category)
                | Q(categories__parent__parent=category)
                | Q(categories__parent__parent__parent=category),
                active=True).distinct()[offset + limit:offset + limit + limit].count()
        elif brand is not None:
            brand = int(brand)
            products = Product.objects.filter(
                Q(brand=brand),
                active=True).distinct()[offset:offset + limit]
            next_products = Product.objects.filter(
                brand=brand,
                active=True).distinct()[offset + limit:offset + limit + limit].count()
        else:
            products = Product.objects.filter(
                active=True).distinct()[offset:offset + limit]
            next_products = Product.objects.filter(
                active=True
            ).distinct()[offset + limit:offset + limit + limit].count()
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
                        'upscale': True,
                        'background': "#ffffff"
                    }).url
            elif produit.images.first():
                data['image'] = get_thumbnailer(
                    produit.images.first()).get_thumbnail({
                        'size': (540, 600),
                        'upscale': True,
                        'background': "#ffffff"
                    }).url
            else:
                data['image'] = None
            if produit.filters.all():
                data['filters'] = " ".join(
                    [slugify(d.name) for d in produit.filters.all()])
            else:
                data['filters'] = None
            if produit.label:
                data['label'] = {}
                data['label']['name'] = produit.label.name
                data['label']['colour'] = produit.label.colour
                data['label']['bg_colour'] = produit.label.bg_colour
            else:
                data['label'] = None
            if hasattr(produit, 'variants'):
                data['variants'] = True
                data['variants_count'] = produit.variants.all().count()
                if produit.variants.first():
                    data['variants_product_code'] = produit.variants.first().product_code
                    data['price'] = produit.variants.first().unit_price
                    data['is_discounted'] = False
                    for v in produit.variants.all():
                        if v.is_discounted:
                            data['is_discounted'] = True
                    data['quantity'] = 0
                    for v in produit.variants.all():
                        if v.quantity > 0:
                            data['quantity'] = v.quantity
                else:
                    data['variants_product_code'] = ""
                    data['price'] = "-"
                    data['is_discounted'] = False
                    data['quantity'] = 0
            else:
                data['price'] = produit.get_price(request)
                data['realprice'] = produit.unit_price
                data['variants'] = False
                data['variants_count'] = 0
                data['is_discounted'] = produit.is_discounted
                data['quantity'] = produit.quantity
            all_produits.append(data)
        # ===---
        result = {"products": all_produits, "next": next_products}
        return RestResponse(result)


class LoadProductsByCategory(APIView):
    """
    Retrieve products for plugin Products by Category.
    """

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):  # noqa: C901
        category = request.GET.get("category", None)
        products = None
        all_produits = []
        if category is not None:
            category = int(category)
            products = Product.objects.filter(
                Q(categories=category) | Q(categories__parent=category)
                | Q(categories__parent__parent=category)
                | Q(categories__parent__parent__parent=category),
                active=True
            ).distinct()[:8]
            # ===---
            all_produits = []
            for produit in products:
                data = {}
                data['name'] = produit.product_name
                data['url'] = produit.get_absolute_url()
                data['caption'] = strip_tags(Truncator(produit.caption).words(18))
                data['slug'] = produit.slug
                if produit.main_image:
                    try:
                        data['image'] = get_thumbnailer(
                            produit.main_image).get_thumbnail({
                                'size': (540, 600),
                                'upscale': True,
                                'background': "#ffffff"
                            }).url
                    except Exception:
                        data['image'] = None
                elif produit.images.first():
                    try:
                        data['image'] = get_thumbnailer(
                            produit.images.first()).get_thumbnail({
                                'size': (540, 600),
                                'upscale': True,
                                'background': "#ffffff"
                            }).url
                    except Exception:
                        data['image'] = None
                else:
                    data['image'] = None
                if produit.filters.all():
                    data['filters'] = " ".join(
                        [slugify(d.name) for d in produit.filters.all()])
                else:
                    data['filters'] = None
                if produit.label:
                    data['label'] = {}
                    data['label']['name'] = produit.label.name
                    data['label']['colour'] = produit.label.colour
                    data['label']['bg_colour'] = produit.label.bg_colour
                else:
                    data['label'] = None
                if hasattr(produit, 'variants'):
                    data['variants'] = True
                    data['variants_count'] = produit.variants.all().count()
                    if produit.variants.first():
                        data['variants_product_code'] = produit.variants.first().product_code
                        data['price'] = produit.variants.first().unit_price
                        data['is_discounted'] = False
                        for v in produit.variants.all():
                            if v.is_discounted:
                                data['is_discounted'] = True
                        data['quantity'] = 0
                        for v in produit.variants.all():
                            if v.quantity > 0:
                                data['quantity'] = v.quantity
                    else:
                        data['variants_product_code'] = ""
                        data['price'] = "-"
                        data['is_discounted'] = False
                        data['quantity'] = 0
                else:
                    data['price'] = produit.get_price(request)
                    data['realprice'] = produit.unit_price
                    data['variants'] = False
                    data['variants_count'] = 0
                    data['is_discounted'] = produit.is_discounted
                    data['quantity'] = produit.quantity
                all_produits.append(data)

        # ===---
        result = {"products": all_produits}
        return RestResponse(result)


class LoadVariantSelect(APIView):
    """
    Retrieve product from attribute selected.
    """

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):  # noqa: C901
        product_pk = request.GET.get("product", None)
        attributes = request.GET.get("attributes", None)
        variants = []
        QUOTATION = False
        try:
            QUOTATION = QUOTATION_FEATURE
        except:
            pass
        if product_pk is not None and attributes is not None:
            attributes = attributes.replace(",", "//separator//").replace("//comma//", ",")
            product = Product.objects.get(pk=product_pk)
            attrs = AttributeValue.objects.filter(
                value__in=attributes.split("//separator//")
            )
            if attrs.count() > 0:
                variant_all = product.variants.all()
            else:
                variant_all = []
            for a in attrs:
                variant_all = variant_all.filter(
                    attribute=a
                )
            for v in variant_all:
                datas = {}
                datas["product_code"] = v.product_code
                datas["unit_price"] = v.unit_price
                datas["quotation"] = 0
                if QUOTATION and v.unit_price == Money(0.01):
                    datas["quotation"] = 1
                try:
                    datas["real_price"] = v.get_price(request)
                except Exception:
                    datas["real_price"] = v.unit_price
                datas["is_discounted"] = v.is_discounted
                datas["quantity"] = v.quantity
                variants.append(datas)
        # ===---
        result = {"variants": variants}
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
        # ===---
        tos = Title.objects.filter(page__reverse_id="terms-and-conditions", language=request.LANGUAGE_CODE)
        if tos.count() > 0:
            tos = "/"+request.LANGUAGE_CODE+"/"+str(tos.first().slug)
        else:
            tos = ""
        # ===---
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
                address_billing if address_billing is not None else {},
                "tos": tos
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
                },
                "tos": tos
            })


class CustomerCheckView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        email = data.get("email", None)
        if email is not None:
            customer = Customer.objects.filter(email=email).count()
            if customer > 0:
                return RestResponse({"exist": True})
            else:
                return RestResponse({"exist": False})
        else:
            return RestResponse({"valid": False})


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
                _("You successfully been added to our newsletter.")
            )
        except Exception as e:
            print(e)
            messages.error(request, _("An error occurred, sorry."))
            redirect("/")
    else:
        messages.error(request, _("Your answer was wrong."))
    return redirect("/")


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
        'Bonjour, voici le message:\n\nNom: ' + request.POST.get('name')
        + '\nCourriel: ' + request.POST.get('email') + '\nTéléphone: '
        + request.POST.get('phone') + '\nSujet: ' + request.POST.get('subject')
        + '\nMessage:\n' + request.POST.get('message'),
        DEFAULT_FROM_EMAIL,
        [DEFAULT_TO_EMAIL],
        fail_silently=False,
    )
    call_command('send_queued_mail')
    return redirect('/message-envoye/')


#######################################################################
# Password Reset
#######################################################################


class PasswordResetConfirmView(GenericAPIView):
    renderer_classes = (CMSPageRenderer, JSONRenderer, BrowsableAPIRenderer)
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)
    form_name = 'password_reset_confirm_form'

    def post(self, request, uidb64=None, token=None):
        try:
            data = dict(request.data['form_data'])
        except (KeyError, TypeError, ValueError):
            errors = {'non_field_errors': [_("Invalid POST data.")]}
        else:
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response_data = {self.form_name: {
                    'success_message': _(
                        "Password has been reset with the new password."
                    ),
                }}
                return RestResponse(response_data)
            else:
                errors = serializer.errors
        return RestResponse({
            self.form_name: errors
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@csrf_exempt
def unclone_customers(request):
    data = json.loads(request.body)["form_data"]
    email = data.get("email", None)
    if email is not None:
        users = User.objects.filter(email=email)
        if users.count() > 1:
            i = 0
            for u in users:
                if i > 0:
                    u.email = ""
                    u.save()
                i = i + 1
    return HttpResponse(json.dumps({"valid": True}))


def send_queued_mail(request):
    call_command('send_queued_mail')
    return HttpResponse(json.dumps({"valid": True}))
