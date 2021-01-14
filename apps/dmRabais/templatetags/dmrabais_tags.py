from django import template

import pytz
from datetime import datetime
from decimal import Decimal
from django.db.models import Q
from shop.money import Money

from dshop.models import Product, ProductVariableVariant

from apps.dmRabais.models import dmRabaisPerCategory

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
