from django import template

from dshop.models import Product, ProductVariableVariant

register = template.Library()

#######################################################################
# ===---   Rabais
#######################################################################


@register.simple_tag
def product_discount_price(id):
    p = Product.objects.get(pk=id)
    return p.get_price(None)


@register.simple_tag
def product_variant_discount_price(id):
    p = ProductVariableVariant.objects.get(pk=id)
    return p.get_price(None)
