
from django.http import JsonResponse
from haystack.query import SearchQuerySet
from .serializers import *

def search_product(request):

    q = request.GET.get('q', '')
    if q is '':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    all_results = SearchQuerySet().filter(content=q)

    products = [result.pk for result in all_results]
    products = Product.objects.filter(id__in=products)

    serializer_context = {'request': request}
    serializer = ProductSerializer(products, context=serializer_context, many=True)
    return JsonResponse(serializer.data, safe=False)

