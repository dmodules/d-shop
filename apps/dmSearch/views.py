from django.http import JsonResponse
from haystack.query import SearchQuerySet
from .serializers import *


def search_product(request):

    q = request.GET.get('q', '')
    if q is '':
        return JsonResponse({})
    #Temperory don't use this for less products
    #all_results = SearchQuerySet().filter(content=q)

    #products = [result.pk for result in all_results]
    #products = Product.objects.filter(id__in=products)

    #Search from name
    query1 = Product.objects.filter(product_name__contains=q)
    q2 = []
    #Search from description
    for product in Product.objects.all():
        if q in product.get_description:
            q2.append(product.id)
    query2 = Product.objects.filter(id__in=q2)

    query = query1 | query2
    serializer_context = {'request': request}
    serializer = ProductSerializer(query,
                                   context=serializer_context,
                                   many=True)
    return JsonResponse(serializer.data, safe=False)
