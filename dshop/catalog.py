import os

from django.db import models
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language_from_request

from rest_framework import views
from rest_framework import status
from rest_framework import generics
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.response import Response

from cms.views import details

from shop.models.product import ProductModel
from shop.rest.money import JSONRenderer
from shop.rest.renderers import ShopTemplateHTMLRenderer
from shop.serializers.bases import ProductSerializer
from shop.serializers.defaults.catalog import AddToCartSerializer


class AddToCartView(views.APIView):
    """
    Handle the "Add to Cart" dialog on the products detail page.
    """
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    product_model = ProductModel
    serializer_class = AddToCartSerializer
    lookup_field = lookup_url_kwarg = 'slug'
    limit_choices_to = models.Q()

    def get_context(self, request, **kwargs):
        assert self.lookup_url_kwarg in kwargs
        filter_kwargs = {self.lookup_field: kwargs.pop(self.lookup_url_kwarg)}
        if hasattr(self.product_model, 'translations'):
            filter_kwargs.update(
                translations__language_code=get_language_from_request(
                    self.request
                )
            )
        queryset = self.product_model.objects.filter(slug=self.kwargs["slug"])
        product = get_object_or_404(queryset)
        return {'product': product, 'request': request}

    def get(self, request, *args, **kwargs):
        context = self.get_context(request, **kwargs)
        serializer = self.serializer_class(context=context, **kwargs)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        context = self.get_context(request, **kwargs)
        serializer = self.serializer_class(data=request.data, context=context)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductRetrieveView(generics.RetrieveAPIView):

    renderer_classes = (
        ShopTemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer
    )
    lookup_field = lookup_url_kwarg = 'slug'
    product_model = ProductModel
    serializer_class = ProductSerializer
    limit_choices_to = models.Q()
    use_modal_dialog = True

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            if request.current_page.node.is_root():
                return details(request, kwargs.get('slug'))
            raise
        except Exception:
            raise

    def get_template_names(self):
        product = self.get_object()
        app_label = product._meta.app_label.lower()
        basename = '{}-detail.html'.format(product._meta.model_name)
        return [
            os.path.join(app_label, 'catalog', basename),
            os.path.join(app_label, 'catalog/product-detail.html'),
            'shop/catalog/product-detail.html',
        ]

    def get_renderer_context(self):
        renderer_context = super().get_renderer_context()
        if renderer_context['request'].accepted_renderer.format == 'html':
            # add the product as Python object to the context
            product = self.get_object()
            renderer_context.update(
                app_label=product._meta.app_label.lower(),
                product=product,
                use_modal_dialog=self.use_modal_dialog,
            )
        return renderer_context

    def get_object(self):
        if not hasattr(self, '_product'):
            assert self.lookup_url_kwarg in self.kwargs
            filter_kwargs = {
                'active': True,
                self.lookup_field: self.kwargs[self.lookup_url_kwarg],
            }
            if hasattr(self.product_model, 'translations'):
                filter_kwargs.update(
                    translations__language_code=get_language_from_request(
                        self.request
                    )
                )
            queryset = self.product_model.objects.filter(
                slug=self.kwargs["slug"]
            )
            self._product = get_object_or_404(queryset)
        return self._product
