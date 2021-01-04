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
    r = Money(0)
    # ===--- GET DISCOUNTS
    today = pytz.utc.localize(datetime.utcnow())
    all_discounts = dmRabaisPerCategory.objects.filter(
        Q(categories__in=p.categories.all()) & Q(is_active=True) & (
            Q(valid_from__isnull=True) | Q(valid_from__lte=today)
        ) & (
            Q(valid_until__isnull=True) | Q(valid_until__gt=today)
        )
    )
    if all_discounts.count() > 0:
        r = p.unit_price
        for d in all_discounts:
            if d.amount is not None:
                r = Money(Decimal(r) - Decimal(d.amount))
            elif d.percent is not None:
                pourcent = Decimal(d.percent) / Decimal("100")
                discount = Money(Decimal(p.unit_price) * pourcent)
                r = r - discount
    else:
        r = p.unit_price
    if Decimal(r) < 0:
        r = Money(0)
    return r


@register.simple_tag
def product_variant_discount_price(id):
    p = ProductVariableVariant.objects.get(pk=id)
    today = pytz.utc.localize(datetime.utcnow())
    all_discounts = dmRabaisPerCategory.objects.filter(
        Q(categories__in=p.product.categories.all()) & Q(is_active=True) & (
            Q(valid_from__isnull=True) | Q(valid_from__lte=today)
        ) & (
            Q(valid_until__isnull=True) | Q(valid_until__gt=today)
        )
    )
    if all_discounts.count() > 0:
        r = p.unit_price
        for d in all_discounts:
            if d.amount is not None:
                r = Money(Decimal(r) - Decimal(d.amount))
            elif d.percent is not None:
                pourcent = Decimal(d.percent) / Decimal("100")
                discount = Money(Decimal(p.unit_price) * pourcent)
                r = r - discount
    else:
        r = p.unit_price
    if Decimal(r) < 0:
        r = Money(0)
    return r
