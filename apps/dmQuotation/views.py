import pytz
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from shop.models.customer import CustomerModel
from dshop.models import ProductVariableVariant
from .models import dmQuotation, dmQuotationItem
from .serializers import dmQuotationSerializer, dmQuotationItemSerializer


class dmQuotationCartCreateAPI(APIView):

    def post(self, request, *args, **kwargs):
        print(request.GET)
        variant = request.GET.get('variant', '')
        quantity = request.GET.get('quantity', '')
        try:
            variant = ProductVariableVariant.objects.get(product_code=variant)
        except:
            return HttpResponse("ERROR!")
        session = Session.objects.filter(session_key=request.session.session_key)
        if session:
            session = session[0].get_decoded()
            user_id = session['_auth_user_id']
            customer = CustomerModel.objects.get(user__id=user_id)
            if customer is None:
                return HttpResponse('Please Sign in or Sign up for Quotation')
            print(customer)

            # Check for Quotation
            quotation = dmQuotation.objects.filter(
                customer=customer,
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
                    customer=customer,
                    number=number
                )
            else:
                quotation = quotation[0]

            quotation_items = dmQuotationItem.objects.filter(quotation=quotation)
            quotation_items = quotation_items.filter(variant_code=variant.product_code)
            if quotation_items:
                # Update Item
                quotation_items[0].quantity += int(quantity)
                quotation_items[0].save()
            else:
                # Create Item 
                data = {
                    'quotation': quotation,
                    'quantity': quantity,
                    'variant_code': variant.product_code,
                    'product_code': variant.product.square_id,
                    'product_name': variant.product.product_name
                }
                dmQuotationItem.objects.create(**data)
        else:
            return HttpResponse('Please Sign in or Sign up for Quotation')
        return HttpResponse('Added to Quotation')

class dmQuotationListCreateAPI(ListCreateAPIView):

    serializer_class = dmQuotationSerializer
    queryset = dmQuotation.objects.all()
    permission_classes = [AllowAny,]
    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(customer__user=user)
        return queryset

class dmQuotationRetrieve(RetrieveDestroyAPIView):

    serializer_class = dmQuotationSerializer
    permission_classes = [AllowAny,]
    lookup_field = 'pk'
    queryset = dmQuotation.objects.all()

class dmQuotationItemListCreateAPI(ListCreateAPIView):

    serializer_class = dmQuotationItemSerializer
    permission_classes = [AllowAny,]
    queryset = dmQuotationItem.objects.all()

class dmQuotationItemRetrieve(RetrieveUpdateDestroyAPIView):

    serializer_class = dmQuotationItemSerializer
    permission_classes = [AllowAny,]
    lookup_field = 'pk'
    queryset = dmQuotationItem.objects.all()
