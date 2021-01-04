import pytz

from decimal import Decimal
from datetime import datetime

from django.db.models import Q

from shop.money import Money

try:
    from apps.dmRabais.models import dmRabaisPerCategory
except Exception:
    dmRabaisPerCategory = None

def get_apply_discountpercategory(product, current_price):
    r = current_price
    if dmRabaisPerCategory is not None:
        today = pytz.utc.localize(datetime.utcnow())
        try:
            if product.product_model:
                categories = product.categories.all()
        except Exception:
            categories = product.product.categories.all()
        all_discounts = dmRabaisPerCategory.objects.filter(
            Q(categories__in=categories) & Q(is_active=True)
            & (Q(valid_from__isnull=True) | Q(valid_from__lte=today))
            & (Q(valid_until__isnull=True) | Q(valid_until__gt=today))
        )
        if all_discounts.count() > 0:
            for d in all_discounts:
                if d.amount is not None:
                    r = Money(Decimal(r) - Decimal(d.amount))
                elif d.percent is not None:
                    pourcent = Decimal(d.percent) / Decimal("100")
                    discount = Money(
                        Decimal(product.unit_price) * pourcent)
                    r = r - discount
    return r
