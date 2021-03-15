# from haystack.query import SearchQuerySet
from django.conf import settings
from django.shortcuts import render

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import dmPortfolio

class PortfolioListView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        ports = dmPortfolio.objects.filter(active=True).order_by('id')
        column = 3
        ports_data = []
        for port in ports:
            data = {
                'id': port.id,
                'title': port.title,
                'image': port.image.url,
                'description': port.description
            }
            ports_data.append(data)
        return render(request, 'port_list.html', {"data": ports_data, "column":column})
