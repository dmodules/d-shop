
from django.http import JsonResponse
from haystack.query import SearchQuerySet
from .serializers import *

from django.core import serializers

def search_product(request):

    q = request.GET.get('q', '')
    if q is '':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    all_results = SearchQuerySet().filter(content=q)
    products = [result.pk for result in all_results]
    products = Product.objects.filter(id__in=products)
    #serializer = ProductSerializer(products)
    serializer = serializers.serialize("json", [q.object for q in all_results])
    return JsonResponse(serializer, safe=False)

