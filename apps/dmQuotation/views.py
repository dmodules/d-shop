import pytz
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import dmQuotation, dmQuotationItem
from .serializers import dmQuotationSerializer, dmQuotationItemSerializer

class dmQuotationListCreateAPI(ListCreateAPIView):

    serializer_class = dmQuotationSerializer
    queryset = dmQuotation.objects.all()
    permission_classes = [AllowAny,]

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
