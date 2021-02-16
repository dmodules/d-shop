from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.contrib.sessions.models import Session

from easy_thumbnails.files import get_thumbnailer

from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response as RestResponse
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from shop.models.customer import CustomerModel

from dshop.models import ProductVariableVariant, ProductDefault
from dshop.transition import quotation_new_notification
from .models import dmQuotation, dmQuotationItem
from .serializers import dmQuotationSerializer, dmQuotationItemSerializer


class dmQuotationCartMergeAPI(APIView):

    def get(self, request, *args, **kwargs):
        cookie = request.GET.get('cookie', None)
        session = Session.objects.filter(session_key=request.session.session_key)
        customer = None
        if session.count() > 0:
            session = session[0].get_decoded()
            user_id = session.get("_auth_user_id")
            if user_id:
                customer = CustomerModel.objects.get(user__id=user_id)

        if cookie and customer:
            cookie_quotation = dmQuotation.objects.filter(
                cookie=cookie,
                status=1,
                customer=None
            )
            for quot in cookie_quotation:
                quot.customer = customer
                quot.save()
            check_quotation = dmQuotation.objects.filter(customer=customer, status=1)
            if check_quotation.count() > 1:
                first_quotation = check_quotation.order_by('id').first()
                check_quotation = check_quotation.exclude(id=first_quotation.id)
                for quot in check_quotation:
                    for item in dmQuotationItem.objects.filter(quotation=quot):
                        item.quotation = first_quotation
                        item.save()
                    quot.delete()
        return HttpResponse('Ok')

class dmQuotationCartCreateAPI(APIView):

    def post(self, request, *args, **kwargs):    # noqa: C901
        variant = request.GET.get('variant', None)
        product = request.GET.get('product', None)
        quantity = request.GET.get('quantity', '')
        cookie = request.GET.get('cookie', '')
        try:
            if product is not None:
                product_obj = ProductDefault.objects.get(product_code=product)
            elif variant is not None:
                product_obj = ProductVariableVariant.objects.get(product_code=variant)
        except Exception as e:
            print(e)
            return RestResponse({"valid": False})

        customer = None

        if not request.user.is_anonymous:
            customer = CustomerModel.objects.get(user=request.user)

        if not customer:
            session = Session.objects.filter(session_key=request.session.session_key)
            if session.count() > 0:
                session = session[0].get_decoded()
                user_id = session.get('_auth_user_id')
                if user_id:
                    customer = CustomerModel.objects.get(user__id=user_id)

        # Check for Quotation
        quotation = []
        if customer:
            quotation = dmQuotation.objects.filter(
                customer=customer,
                status=1
            ).last()
        if not quotation:
            quotation = dmQuotation.objects.filter(
                cookie=cookie,
                status=1
            ).last()

        if not quotation:
            # To generate Quotation Number
            existing_q = dmQuotation.objects.all().order_by('-id')
            if existing_q:
                number = existing_q.first().number
                number = int(number) + 1
            else:
                number = "00001"
            if len(str(number)) < 5:
                num = '0'
                for i in range(1, 5-len(str(number))):
                    num = str(num) + '0'
                number = num + str(number)
            quotation = dmQuotation.objects.create(
                cookie=cookie,
                customer=customer,
                number=number
            )
        else:
            if customer:
                quotation.customer = customer
                quotation.save()
                '''if cookie:
                    cookie_quotation = dmQuotation.objects.filter(
                        cookie=cookie,
                        status=1,
                        customer=None
                    )
                    for quot in cookie_quotation:
                        quot.customer = customer
                        quot.save()
            check_quotation = dmQuotation.objects.filter(customer=customer, status=1)
            if check_quotation.count() > 1:
                first_quotation = check_quotation.order_by('id').first()
                check_quotation = check_quotation.exclude(id=first_quotation.id)
                for quot in check_quotation:
                    for item in dmQuotationItem.objects.filter(quotation=quot):
                        item.quotation = first_quotation
                        item.save()
                    quot.delete()
                quotation = first_quotation'''

        if product is not None:
            quotation_items = dmQuotationItem.objects.filter(
                quotation=quotation,
                product_code=product_obj.product_code
            )
        if variant is not None:
            quotation_items = dmQuotationItem.objects.filter(
                quotation=quotation,
                variant_code=product_obj.product_code
            )
        if quotation_items:
            # Update Item
            quotation_items[0].quantity += int(quantity)
            quotation_items[0].save()
        else:
            # Create Item
            data = {
                'quotation': quotation,
                'quantity': quantity,
            }
            if variant is not None:
                attributes = ",".join([attr.value for attr in product_obj.attribute.all()])
                data['product_type'] = 2
                data['variant_code'] = product_obj.product_code
                data['variant_attribute'] = attributes
                data['product_code'] = product_obj.product.square_id
                data['product_name'] = product_obj.product.product_name
            else:
                attributes = ''
                data['product_type'] = 1
                data['product_code'] = product_obj.product_code
                data['product_name'] = product_obj.product_name
            dmQuotationItem.objects.create(**data)
        return RestResponse({"valid": True})

class dmQuotationListCreateAPI(ListCreateAPIView):

    serializer_class = dmQuotationSerializer
    queryset = dmQuotation.objects.all()
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(customer__user=user)
        return queryset

class dmQuotationRetrieve(RetrieveUpdateDestroyAPIView):

    serializer_class = dmQuotationSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'pk'
    # queryset = dmQuotation.objects.all()

    def get_queryset(self):
        cust = CustomerModel.objects.get(user=self.request.user)
        query = dmQuotation.objects.filter(
            customer=cust
        )
        return query

    def get(self, request, *args, **kwargs):
        cookie = request.GET.get('cookie', None)
        quotation = None
        if not request.user.is_anonymous:
            quotation = dmQuotation.objects.filter(
                pk=kwargs['pk'],
                customer__user=request.user,
                status=1
            ).last()
        elif cookie is not None:
            quotation = dmQuotation.objects.filter(
                pk=kwargs['pk'],
                cookie=cookie,
                status=1
            ).last()
        else:
            session = Session.objects.filter(session_key=request.session.session_key).last()
            if session.count() > 0:
                session = session[0].get_decoded()
                user_id = session.get('_auth_user_id')
                if user_id:
                    customer = CustomerModel.objects.get(user__id=user_id)
                    quotation = dmQuotation.objects.filter(
                        pk=kwargs['pk'],
                        customer__user=customer,
                        status=1
                    ).last()
        if quotation is None:
            context = {'quotations': [], 'count': 0}
        else:
            quot = {
                'id': quotation.id,
                'number': quotation.number,
                'status': dmQuotation.CHOICE_STATUS[int(quotation.status)-1][0],
                'created_at': quotation.created_at,
                'updated_at': quotation.updated_at
            }
            items = []
            for item in dmQuotationItem.objects.filter(
                quotation=quotation
            ).order_by("product_name"):
                if item.product_type == 1:
                    current_item = ProductDefault.objects.filter(
                        product_code=item.product_code
                    ).first()
                    if current_item.main_image:
                        try:
                            current_image = get_thumbnailer(
                                current_item.main_image
                            ).get_thumbnail({
                                'size': (80, 80),
                                'upscale': True,
                                'background': "#ffffff"
                            }).url
                        except Exception:
                            current_image = None
                    else:
                        current_image = None
                    itm = {
                        'id': item.id,
                        'product_name': item.product_name,
                        'product_code': item.product_code,
                        'product_url': current_item.get_absolute_url(),
                        'product_image': current_image,
                        'variant_attribute': None,
                        'quantity': item.quantity,
                    }
                elif item.product_type == 2:
                    # ===---
                    current_item = ProductVariableVariant.objects.filter(
                        product_code=item.variant_code
                    ).first()
                    if current_item.product.main_image:
                        try:
                            current_image = get_thumbnailer(
                                current_item.product.main_image
                            ).get_thumbnail({
                                'size': (80, 80),
                                'upscale': True,
                                'background': "#ffffff"
                            }).url
                        except Exception:
                            current_image = None
                    else:
                        current_image = None
                    # ===---
                    itm = {
                        'id': item.id,
                        'product_name': item.product_name,
                        'product_code': item.variant_code,
                        'product_url': current_item.product.get_absolute_url(),
                        'product_image': current_image,
                        'variant_attribute': item.variant_attribute,
                        'quantity': item.quantity,
                    }
                items.append(itm)
            quot["items"] = items
            context = {"quotation": quot}
        return RestResponse(context)

    def patch(self, request, *args, **kwargs):
        if 'status' in request.data:
            if request.data['status'] == '2':
                print(request.user)
                print(CustomerModel.objects.get(user=request.user))
                print(args, kwargs)
                print("Send email.")
                quotation = dmQuotation.objects.get(id=kwargs['pk'])
                quotation_new_notification(quotation)
        return self.partial_update(request, *args, **kwargs)

class dmQuotationItemListCreateAPI(ListCreateAPIView):

    serializer_class = dmQuotationItemSerializer
    permission_classes = [AllowAny, ]
    queryset = dmQuotationItem.objects.all()

class dmQuotationItemRetrieve(RetrieveUpdateDestroyAPIView):

    serializer_class = dmQuotationItemSerializer
    permission_classes = [AllowAny, ]
    lookup_field = 'pk'
    queryset = dmQuotationItem.objects.all()

def dmQuotationPage(request):
    cookie = request.GET.get('cookie', '')
    template = loader.get_template(
        "theme/{}/pages/quotation.html".format(settings.THEME_SLUG)
    )

    if request.user:
        quotations = dmQuotation.objects.filter(customer__user=request.user)
    elif cookie:
        quotations = dmQuotation.objects.filter(cookie=cookie)
    else:
        return HttpResponse(template.render({}, request))

    if not quotations:
        context = {'quotations': [], 'count': 0}
    else:
        data = []
        for quotation in quotations:
            quot = {
                'id': quotation.id,
                'number': quotation.number,
                'status': dmQuotation.CHOICE_STATUS[int(quotation.status)-1][1],
                'created_at': quotation.created_at,
                'updated_at': quotation.updated_at
            }
            items = []
            for item in dmQuotationItem.objects.filter(quotation=quotation):
                itm = {
                    'id': item.id,
                    'product_name': item.product_name,
                    'product_code': item.product_code,
                    'variant_code': item.variant_code,
                    'variant_attribute': item.variant_attribute,
                    'quantity': item.quantity,
                }
                items.append(itm)
            quot["items"] = items
            data.append(quot)
        context = {'quotations': data, 'count': len(data)}
    return HttpResponse(template.render(context, request))

class dmQuotationCurrent(APIView):
    def get(self, request, *args, **kwargs):
        cookie = request.GET.get('cookie', None)
        quotation = None
        if not request.user.is_anonymous:
            quotation = dmQuotation.objects.filter(
                customer__user=request.user,
                status=1
            ).last()
        elif cookie is not None:
            quotation = dmQuotation.objects.filter(
                cookie=cookie,
                status=1
            ).last()
        else:
            session = Session.objects.filter(session_key=request.session.session_key)
            if session:
                session = session[0].get_decoded()
                user_id = session['_auth_user_id']
                customer = CustomerModel.objects.get(user__id=user_id)
                quotation = dmQuotation.objects.filter(
                    customer__user=customer,
                    status=1
                ).last()
        if quotation is None:
            context = {'quotations': [], 'count': 0}
        else:
            quot = {
                'id': quotation.id,
                'number': quotation.number,
                'status': dmQuotation.CHOICE_STATUS[int(quotation.status)-1][1],
                'created_at': quotation.created_at,
                'updated_at': quotation.updated_at
            }
            items = []
            for item in dmQuotationItem.objects.filter(
                quotation=quotation
            ).order_by("product_name"):
                if item.product_type == 1:
                    current_item = ProductDefault.objects.filter(
                        product_code=item.product_code
                    ).first()
                    if current_item.main_image:
                        try:
                            current_image = get_thumbnailer(
                                current_item.main_image
                            ).get_thumbnail({
                                'size': (80, 80),
                                'upscale': True,
                                'background': "#ffffff"
                            }).url
                        except Exception:
                            current_image = None
                    else:
                        current_image = None
                    itm = {
                        'id': item.id,
                        'product_name': item.product_name,
                        'product_code': item.product_code,
                        'product_url': current_item.get_absolute_url(),
                        'product_image': current_image,
                        'variant_attribute': None,
                        'quantity': item.quantity,
                    }
                elif item.product_type == 2:
                    # ===---
                    current_item = ProductVariableVariant.objects.filter(
                        product_code=item.variant_code
                    ).first()
                    if current_item.product.main_image:
                        try:
                            current_image = get_thumbnailer(
                                current_item.product.main_image
                            ).get_thumbnail({
                                'size': (80, 80),
                                'upscale': True,
                                'background': "#ffffff"
                            }).url
                        except Exception:
                            current_image = None
                    else:
                        current_image = None
                    # ===---
                    itm = {
                        'id': item.id,
                        'product_name': item.product_name,
                        'product_code': item.variant_code,
                        'product_url': current_item.product.get_absolute_url(),
                        'product_image': current_image,
                        'variant_attribute': item.variant_attribute,
                        'quantity': item.quantity,
                    }
                items.append(itm)
            quot["items"] = items
            context = {"quotation": quot}
        return RestResponse(context)
