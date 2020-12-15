from shop.models.cart import CartModel
from shop.serializers.defaults.catalog import AddToCartSerializer
import json


class AddProductVariableToCartSerializer(AddToCartSerializer):
    """
    Used to correctly retrieve variant of ProductVariable's data
    to be used to send an add to cart request.
    """

    def get_instance(self, context, data, extra_args):
        product = context['product']
        request = context['request']
        code = request.GET.get('product_code', None)
        try:
            cart = CartModel.objects.get_from_request(request)
        except CartModel.DoesNotExist:
            cart = None
        try:
            variant = product.get_product_variant(product_code=code)
        except (TypeError, KeyError, product.DoesNotExist):
            variant = product.variants.first()
        instance = {
            'product': product.id,
            'product_code': variant.product_code,
            'unit_price': variant.unit_price,
            'is_in_cart': bool(
                product.is_in_cart(cart, product_code=variant.product_code)
            ),
            'availability': variant.get_availability(request)
        }
        return instance
