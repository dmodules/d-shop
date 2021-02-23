import re
import json

from mailchimp3 import MailChimp
from easy_thumbnails.files import get_thumbnailer
from ipware.ip import get_client_ip as get_ip

from cms.models import Title
from django.db.models.functions import Lower
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language_from_request
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import slugify
from django.core.management import call_command
from django.core.mail import send_mail
from django.db.models import Q

from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response as RestResponse
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from shop.money import Money
from shop.models.defaults.customer import Customer
from shop.modifiers.pool import cart_modifiers_pool
from shop.models.order import OrderModel
from shop.models.order import OrderPayment
from shop.money import MoneyMaker
from shop.rest.renderers import CMSPageRenderer
from shop.views.order import OrderView
from shop.serializers.auth import PasswordResetConfirmSerializer

from dal import autocomplete

from dshop.models import Product, ProductFilterGroup, ProductFilter
from dshop.models import Attribute, AttributeValue, ProductCategory, ProductBrand
from dshop.transition import transition_change_notification
from dshop.serializers import ProductSerializer

from settings import DEFAULT_FROM_EMAIL, DEFAULT_TO_EMAIL, THEME_SLUG
from settings import MAILCHIMP_KEY, MAILCHIMP_LISTID

from feature_settings import QUOTATION


try:
    from apps.dmRabais.models import dmCustomerPromoCode
except ImportError:
    dmCustomerPromoCode = None

#######################################################################
# ===---   OrderView Bug fix                                   ---=== #
#######################################################################


class OrderPermission(BasePermission):
    """
    Allow access to a given Order if the user is entitled to.
    """
    def has_permission(self, request, view):
        if view.many and request.customer.is_visitor:
            detail = _("Only signed in customers can view their list of orders.")
            raise PermissionDenied(detail=detail)
        return True

    def has_object_permission(self, request, view, order):
        if request.user.is_authenticated and not request.user.is_staff and not request.user.is_superuser:
            return order.customer.pk == request.user.pk
        if order.secret and order.secret == view.kwargs.get('secret') or request.user.is_staff or request.user.is_superuser:
            return True
        detail = _("This order does not belong to you.")
        raise PermissionDenied(detail=detail)


class OrderView(OrderView):

    permission_classes = [OrderPermission]

    def get_queryset(self):
        queryset = OrderModel.objects.all()
        if self.request.customer.user.is_staff or self.request.customer.user.is_superuser:
            return queryset
        if self.request.customer.is_visitor:
            return queryset.none()
        if self.request.customer.is_authenticated:
            queryset = queryset.filter(customer=self.request.customer).order_by('-updated_at')
        return queryset


#######################################################################
# ===---   TestPaymentView                                     ---=== #
#######################################################################


def TestPaymentView(request):  # noqa: C901
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
            OrderPayment.objects.create(order=order,
                                        amount=amount,
                                        transaction_id=transactionId,
                                        payment_method="Test (development)")
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
                                promocode__code=pm)
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
                    "url": "/vos-commandes/" + str(referenceId) + "/" + str(order.token),
                    "items": items,
                    "extra": order.extra,
                    "subtotal": order.subtotal,
                    "total": order.total,
                    "billing_address_text": order.billing_address_text,
                    "shipping_address_text": order.shipping_address_text
                }
                transition_change_notification(order, miniorder)
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

class DshopProductListView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        attribute = self.request.query_params.get('attribute', None)
        category = self.request.query_params.get('category', None)
        fltr = self.request.query_params.get('filter', None)
        brand = self.request.query_params.get('brand', None)
        response_type = self.request.query_params.get('type', None)
        offset = int(request.GET.get("offset", 0))
        limit = int(request.GET.get("limit", 9))
        sortby = request.COOKIES.get("dm_psortby", "default")
        if sortby == "date-new":
            orderby = "-created_at"
        elif sortby == "date-old":
            orderby = "created_at"
        elif sortby == "alpha-asc":
            orderby = Lower("product_name")
        elif sortby == "alpha-des":
            orderby = Lower("product_name").desc()
        elif sortby == "price-asc":
            orderby = "get_p"
        elif sortby == "price-des":
            orderby = "-get_p"
        else:
            orderby = "order"

        products = Product.objects.filter(
            Q(categories__active=True) | Q(categories=None),
            active=True
        )
        title = 'Produits'
        current_category = None
        current_brand = None
        if 'category_id' in kwargs:
            products = products.filter(categories__id=kwargs['category_id'])
            cat = ProductCategory.objects.filter(id=kwargs['category_id']).first()
            if cat:
                current_category = cat
                title = cat.name
        elif 'brand_id' in kwargs:
            products = products.filter(brand=kwargs['brand_id'])
            brnd = ProductBrand.objects.filter(id=kwargs['brand_id']).first()
            if brnd:
                current_brand = brnd
                title = brnd.name

        if category:
            category = [ val for val in category.split(',') if val ]
            products = products.filter(categories__id__in=category).distinct()

        if fltr:
            fltr = [ val for val in fltr.split(',') if val ]
            products = products.filter(filters__id__in=fltr).distinct()

        if brand:
            brand = [ val for val in brand.split(',') if val ]
            products = products.filter(brand__id__in=brand).distinct()

        if attribute:
            attributes = [ val for val in attribute.split(',') if val ]
            attributes = AttributeValue.objects.filter(id__in=attributes)
            attributes = [ atr.value for atr in attributes ]
            ids = []
            for q in products:
                attrs = []
                try:
                    for var in q.variants.all():
                        attrs += [val[0] for val in var.attribute.all().values_list('value')]
                except Exception:
                    continue

                for atr in attributes:
                    if atr in attrs:
                        ids.append(q.id)
                        break
            products = Product.objects.filter(id__in=ids)
        
        if orderby == 'get_p':
            products = sorted(
                products, key=lambda product: product.get_price(request)
            )
        elif orderby == '-get_p':
            products = sorted(
                products, key=lambda product: product.get_price(request),
                reverse=True
            )
        else:
            products = products.order_by(orderby)
        categories = ProductCategory.objects.filter(parent=None, active=True)
        brands = ProductBrand.objects.all()
        filters = ProductFilter.objects.all()
        next_page = False

        if len(products) > offset + limit:
            products = products[ offset : limit]
            next_page = True
        else:
            products = products[ offset : ]
        filter_data = LoadFilters.as_view()(request=request._request).data
        data = {
            'products': products,
            'brands': brands,
            'categories': categories,
            'filters': filters,
            'filter_data': filter_data,
            'is_quotation': QUOTATION,
            'title_str': title,
            'current_category': current_category,
            'current_brand': current_brand,
            'next': next_page
        }

        if not response_type:
            return render(request,
                'theme/{}/pages/produits.html'.format(THEME_SLUG),
                context=data
            )
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
                        'upscale':
                        True,
                        'background':
                        "#ffffff"
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
                    data['variants_product_code'] = produit.variants.first(
                    ).product_code
                    data['price'] = produit.variants.first().get_price(request)
                    data['realprice'] = produit.variants.first().unit_price
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
                data['product_code'] = produit.product_code
                data['price'] = produit.get_price(request)
                data['realprice'] = produit.unit_price
                data['variants'] = False
                data['variants_count'] = 0
                data['is_discounted'] = produit.is_discounted
                data['quantity'] = produit.quantity
            data['is_quotation'] = QUOTATION
            all_produits.append(data)
        # ===---
        result = {"products": all_produits, "next": next_page}
        return RestResponse(result)


class LoadFilters(APIView):

    def get(self, request, *args, **kwargs):
        groups = ProductFilterGroup.objects.all()
        data = {}
        # ===--- Filters with group
        for group in groups:
            temp = {}
            filters = []
            temp['id'] = group.id
            temp['order'] = group.order
            for filt in ProductFilter.objects.filter(group=group):
                url = ''
                if filt.image:
                    url = filt.image.url
                filters.append({
                    'id': filt.id,
                    'name': filt.name,
                    'order': filt.order,
                    'image': url,
                    'description': filt.description
                })
            temp['filter'] = filters
            data[group.name] = temp
        temp = {}
        # ===--- Filters without group
        filters = []
        for filt in ProductFilter.objects.filter(group=None):
            filters.append({'id': filt.id, 'name': filt.name, 'order': filt.order})
        data['default'] = {'filter': filters}
        # ===---

        a_data = {}
        for attr in Attribute.objects.all():
            a_data[attr.name] = {}
            a_data[attr.name]["id"] = attr.id
            a_data[attr.name]["values"] = []
            for val in AttributeValue.objects.filter(attribute=attr):
                a_data[attr.name]["values"].append({
                    'id': val.id,
                    'name': val.value
                })

        categories = ProductCategory.objects.filter(parent=None, active=True)
        cat_data = []
        for cat in categories:
            cat_d = {'id': cat.id, 'name': cat.name}
            child_c = []
            for child in ProductCategory.objects.filter(parent=cat, active=True):
                child_c.append({'id': child.id, 'name': child.name})
            cat_d['child'] = child_c
            cat_data.append(cat_d)

        brands = []
        for brand in ProductBrand.objects.all():
            brands.append({'id': brand.id, 'name': brand.name})

        return RestResponse({
            'filter': data,
            'attribute': a_data,
            'categories': cat_data,
            'brands': brands
        })


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

    def get(self, request, *args, **kwargs):  # noqa: C901
        category = request.GET.get("category", None)
        brand = request.GET.get("brand", None)
        offset = int(request.GET.get("offset", 0))
        limit = int(request.GET.get("limit", 2))
        # ===---
        sortby = request.COOKIES.get("dm_psortby", "default")
        if sortby == "date-new":
            orderby = "-created_at"
        elif sortby == "date-old":
            orderby = "created_at"
        elif sortby == "alpha-asc":
            orderby = "product_name"
        elif sortby == "alpha-des":
            orderby = "-product_name"
        elif sortby == "price-asc":
            orderby = "order"
        elif sortby == "price-des":
            orderby = "order"
        else:
            orderby = "order"
        # ===---
        try:
            is_quotation = QUOTATION_FEATURE
        except Exception:
            is_quotation = False
        if category is not None:
            category = int(category)
            products = Product.objects.filter(
                Q(categories=category) | Q(categories__parent=category)
                | Q(categories__parent__parent=category)
                | Q(categories__parent__parent__parent=category),
                active=True).order_by(orderby).distinct()
            next_products = Product.objects.filter(
                Q(categories=category) | Q(categories__parent=category)
                | Q(categories__parent__parent=category)
                | Q(categories__parent__parent__parent=category), active=True
            ).order_by(orderby).distinct()[
                offset + limit:offset + limit + limit
            ].count()
        elif brand is not None:
            brand = int(brand)
            products = Product.objects.filter(
                Q(brand=brand), active=True
            ).order_by(orderby).distinct()
            next_products = Product.objects.filter(
                brand=brand, active=True
            ).order_by(orderby).distinct()[
                offset + limit:offset + limit + limit
            ].count()
        else:
            products = Product.objects.filter(
                Q(categories__active=True) | Q(categories=None),
                active=True
            ).order_by(orderby).distinct()
            next_products = Product.objects.filter(
                Q(categories__active=True) | Q(categories=None),
                active=True
            ).order_by(orderby).distinct()[
                offset + limit:offset + limit + limit
            ].count()
        # ===---
        if sortby == "price-asc":
            products = sorted(
                products, key=lambda t: t.get_price(request)
            )
        elif sortby == "price-des":
            products = sorted(
                products, key=lambda t: t.get_price(request),
                reverse=True
            )
        # ===---
        products = products[offset:offset+limit]
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
                        'upscale':
                        True,
                        'background':
                        "#ffffff"
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
                    data['variants_product_code'] = produit.variants.first(
                    ).product_code
                    data['price'] = produit.variants.first().get_price(request)
                    data['realprice'] = produit.variants.first().unit_price
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
                data['product_code'] = produit.product_code
                data['price'] = produit.get_price(request)
                data['realprice'] = produit.unit_price
                data['variants'] = False
                data['variants_count'] = 0
                data['is_discounted'] = produit.is_discounted
                data['quantity'] = produit.quantity
            data['is_quotation'] = is_quotation
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
        try:
            is_quotation = QUOTATION_FEATURE
        except Exception:
            is_quotation = False
        if category is not None:
            category = int(category)
            products = Product.objects.filter(
                Q(categories=category) | Q(categories__parent=category)
                | Q(categories__parent__parent=category)
                | Q(categories__parent__parent__parent=category),
                active=True).distinct()[:8]
            # ===---
            all_produits = []
            for produit in products:
                data = {}
                data['name'] = produit.product_name
                data['url'] = produit.get_absolute_url()
                data['caption'] = strip_tags(
                    Truncator(produit.caption).words(18))
                data['slug'] = produit.slug
                if produit.main_image:
                    try:
                        data['image'] = get_thumbnailer(
                            produit.main_image).get_thumbnail({
                                'size': (540, 600),
                                'upscale':
                                True,
                                'background':
                                "#ffffff"
                            }).url
                    except Exception:
                        data['image'] = None
                elif produit.images.first():
                    try:
                        data['image'] = get_thumbnailer(
                            produit.images.first()).get_thumbnail({
                                'size': (540, 600),
                                'upscale':
                                True,
                                'background':
                                "#ffffff"
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
                        data['variants_product_code'] = produit.variants.first(
                        ).product_code
                        data['price'] = produit.variants.first().get_price(request)
                        data['realprice'] = produit.variants.first().unit_price
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
                    data['product_code'] = produit.product_code
                    data['price'] = produit.get_price(request)
                    data['realprice'] = produit.unit_price
                    data['variants'] = False
                    data['variants_count'] = 0
                    data['is_discounted'] = produit.is_discounted
                    data['quantity'] = produit.quantity
                data['is_quotation'] = is_quotation
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
        except Exception:
            pass
        if product_pk is not None and attributes is not None:
            attributes = attributes.replace(",", "//separator//").replace(
                "//comma//", ",")
            product = Product.objects.get(pk=product_pk)
            attr_list = attributes.split("//separator//")
            attrs = AttributeValue.objects.none()
            for a in attr_list:
                attrs |= AttributeValue.objects.filter(
                    value=a.split("_____")[1],
                    attribute__name=a.split("_____")[0]
                )
            print(attrs)
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
                if QUOTATION:
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
        tos = Title.objects.filter(page__reverse_id="terms-and-conditions",
                                   language=request.LANGUAGE_CODE)
        if tos.count() > 0:
            tos = "/" + request.LANGUAGE_CODE + "/" + str(tos.first().slug)
        else:
            tos = ""
        # ===---
        is_visitor = True if request.customer.is_visitor else False
        # ===---
        if request.user.is_authenticated:
            customer = {
                "salutation": request.user.customer.salutation,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
                "is_visitor": is_visitor
            }
            aso = request.user.customer.shippingaddress_set.first()
            if aso is not None:
                address_shipping = {
                    "active_priority": 1,
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
                    "guest": True,
                    "is_visitor": is_visitor
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
        email = request.data.get("email", None)
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
                request, _("You successfully been added to our newsletter."))
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


#######################################################################
# Password Reset
#######################################################################


class PasswordResetConfirmView(GenericAPIView):
    renderer_classes = (CMSPageRenderer, JSONRenderer, BrowsableAPIRenderer)
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny, )
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
                response_data = {
                    self.form_name: {
                        'success_message':
                        _("Password has been reset with the new password."),
                    }
                }
                return RestResponse(response_data)
            else:
                errors = serializer.errors
        return RestResponse({self.form_name: errors},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)


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


class AttributeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return AttributeValue.objects.none()

        qs = AttributeValue.objects.all()

        if self.q:
            qs = qs.filter(Q(value__istartswith=self.q) | Q(attribute__name__istartswith=self.q))

        return qs
