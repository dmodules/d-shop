from rest_framework import serializers

from shop.serializers.bases import ProductSerializer as ShopProductSerializer
from shop.models.cart import CartModel
from shop.serializers.defaults.catalog import AddToCartSerializer
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class AddProductVariableToCartSerializer(AddToCartSerializer):
    """
    Used to correctly retrieve variant of ProductVariable's data
    to be used to send an add to cart request.
    """
    def get_instance(self, context, data, extra_args):
        product = context["product"]
        request = context["request"]
        code = request.GET.get("product_code", None)
        try:
            cart = CartModel.objects.get_from_request(request)
        except CartModel.DoesNotExist:
            cart = None
        try:
            variant = product.get_product_variant(product_code=code)
        except (TypeError, KeyError, product.DoesNotExist):
            variant = product.variants.first()
        instance = {
            "product": product.id,
            "product_code": variant.product_code,
            "unit_price": variant.unit_price,
            "is_in_cart": bool(product.is_in_cart(cart, product_code=variant.product_code)),
            "availability": variant.get_availability(request)
        }
        return instance


class ExtraCartRowContent(serializers.Serializer):
    """
    This data structure holds extra information for each item, or for the whole cart, while
    processing the cart using their modifiers.
    """
    label = serializers.CharField(
        read_only=True,
        help_text="A short description of this row in a natural language.",
    )

    content = serializers.CharField(
        help_text="Content of the data.",
    )

    content_extra = serializers.CharField(
        help_text="Extra content of the data.",
    )


class dmProductSummarySerializer(ShopProductSerializer):
    media = serializers.SerializerMethodField(
        help_text="Returns a rendered HTML snippet",
    )

    caption = serializers.SerializerMethodField(
        help_text="Returns the content from caption field if available",
    )

    class Meta(ProductSerializer.Meta):
        fields = [
            'id',
            'product_name',
            'product_name_trans',
            'product_url',
            'product_model',
            'price',
            'media',
            'caption'
        ]

    def get_media(self, product):
        return self.render_html(product, 'media')

    def get_caption(self, product):
        return getattr(product, 'caption', None)
