# from haystack.query import SearchQuerySet
from django.shortcuts import render

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import dmPortfolio

class PortfolioListView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        portfolios = dmPortfolio.objects.filter(active=True).order_by('id')
        column = 3
        portfolio_data = []
        for p in portfolios:
            data = {
                'id': p.id,
                'title': p.title,
                'image': p.image.url,
                'description': p.description
            }
            portfolio_data.append(data)
        return render(request, 'portfolio_list.html', {"data": portfolio_data, "column": column})
