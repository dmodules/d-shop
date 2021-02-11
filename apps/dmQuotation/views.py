import pytz
from django.http import HttpResponse
from django.template import loader
from django.contrib.sessions.models import Session
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response as RestResponse
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from shop.models.customer import CustomerModel
from django.conf import settings
from dshop.models import ProductVariableVariant
from .models import dmQuotation, dmQuotationItem
from .serializers import dmQuotationSerializer, dmQuotationItemSerializer


class dmQuotationCartCreateAPI(APIView):

    def post(self, request, *args, **kwargs):
        variant = request.GET.get('variant', '')
        quantity = request.GET.get('quantity', '')
        cookie = request.GET.get('cookie', '')

        try:
            variant = ProductVariableVariant.objects.get(product_code=variant)
        except Exception as e:
            print(e)
            return RestResponse({"valid": False})

        session = Session.objects.filter(session_key=request.session.session_key)
        customer = None
        if session:
            session = session[0].get_decoded()
            user_id = session['_auth_user_id']
            customer = CustomerModel.objects.get(user__id=user_id)

        # Check for Quotation
        quotation = dmQuotation.objects.filter(
            cookie=cookie,
            status=1
        )
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
            quotation = quotation[0]
            if customer:
                quotation.customer = customer
                quotation.save()

        quotation_items = dmQuotationItem.objects.filter(quotation=quotation)
        quotation_items = quotation_items.filter(variant_code=variant.product_code)
        if quotation_items:
            # Update Item
            quotation_items[0].quantity += int(quantity)
            quotation_items[0].save()
        else:
            # Create Item
            attributes = ",".join([attr.value for attr in variant.attribute.all()])
            data = {
                'quotation': quotation,
                'quantity': quantity,
                'variant_code': variant.product_code,
                'variant_attribute': attributes,
                'product_code': variant.product.square_id,
                'product_name': variant.product.product_name
            }
            dmQuotationItem.objects.create(**data)
        return RestResponse({"valid": True})

class dmQuotationListCreateAPI(ListCreateAPIView):

    serializer_class = dmQuotationSerializer
    queryset = dmQuotation.objects.all()
    permission_classes = [AllowAny,]
    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(customer__user=user)
        return queryset

class dmQuotationRetrieve(RetrieveUpdateDestroyAPIView):

    serializer_class = dmQuotationSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'pk'
    queryset = dmQuotation.objects.all()

    def patch(self, request, *args, **kwargs):
        if 'status' in request.data:
            if request.data['status'] == '2':
                print(request.user)
                print(CustomerModel.objects.get(user=request.user))
                print("Send email.")
        return self.partial_update(request, *args, **kwargs)

class dmQuotationItemListCreateAPI(ListCreateAPIView):

    serializer_class = dmQuotationItemSerializer
    permission_classes = [AllowAny,]
    queryset = dmQuotationItem.objects.all()

class dmQuotationItemRetrieve(RetrieveUpdateDestroyAPIView):

    serializer_class = dmQuotationItemSerializer
    permission_classes = [AllowAny,]
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
        cookie = request.GET.get('cookie', '')

        if request.user:
            quotation = dmQuotation.objects.filter(
                customer__user=request.user,
                status=1
            ).last()
        elif cookie:
            quotation = dmQuotation.objects.filter(
                cookie=cookie,
                status=1
            ).last()

        if not quotation:
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
            context = {"quotation": quot}
        return RestResponse(context)
