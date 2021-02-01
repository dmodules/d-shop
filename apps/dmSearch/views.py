# from haystack.query import SearchQuerySet
import json
import math

from django.http import HttpResponse
from django.template import loader
from django.conf import settings

from .serializers import ProductSerializer

from dshop.models import Product


def search_product(request):
    q = request.GET.get('q', None)
    page = int(request.GET.get('page', '1'))
    limit = 2
    #
    template = loader.get_template(
        "theme/{}/pages/search.html".format(settings.THEME_SLUG)
    )
    #
    if q is not None:
        # Search from name
        query1 = Product.objects.filter(product_name__icontains=q)
        # Search from caption
        q2 = []
        for product in Product.objects.all():
            if q in product.get_caption:
                q2.append(product.id)
        query2 = Product.objects.filter(id__in=q2)
        # Search from description
        q3 = []
        for product in Product.objects.all():
            if q in product.get_description:
                q3.append(product.id)
        query3 = Product.objects.filter(id__in=q3)
        # Render
        query = query1 | query2 | query3
        serializer_context = {'request': request}
        serializer = ProductSerializer(
            query,
            context=serializer_context,
            many=True
        )
        products = []
        for p in serializer.data:
            products.append(Product.objects.get(
                id=json.loads(json.dumps(p))["id"]
            ))
        context = {
            "query": q,
            "products": products[(page * limit - limit):(page * limit)],
            "next": True if len(
                products[
                    ((page + 1) * limit - limit):((page + 1) * limit)
                ]
            ) > 0 else False,
            "pages": math.ceil(len(products) / limit),
            "page": page,
            "count": len(products)
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse(template.render({}, request))
