import re
import pytz

from decimal import Decimal
from datetime import datetime

from geopy.geocoders import Nominatim

from django.db.models import Q

from shop.money import Money

try:
    from apps.dmRabais.models import dmRabaisPerCategory
except Exception:
    dmRabaisPerCategory = None


def get_coords_from_address(address):
    geolocator = Nominatim(user_agent="dshop")
    location = geolocator.geocode(address)
    if location:
        return location
    else:
        try:
            postalcode = re.findall(r"[A-Za-z]{1}[0-9]{1}[A-Za-z]{1} [0-9]{1}[A-Za-z]{1}[0-9]{1}", address)[0]
            postal_location = get_coords_from_address(postalcode)
        except Exception:
            postal_location = None
        if postal_location:
            return postal_location
        else:
            new_addr = address.split(",")
            if len(new_addr) > 1:
                new_addr = ",".join(new_addr[:-1])
                new_addr = re.sub(r"\([^()]*\)", "", new_addr)
                get_coords_from_address(new_addr)
            else:
                return location

def get_apply_discountpercategory(product, current_price, is_discounted=False):  # noqa: C901
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
                # 1. if Can apply dmRabaisPerCategory on discounted product
                #        Calculate Product
                #    else continue
                # 2. if Can not apply dmRabaisPerCategory on discounted product
                #        Check if product is discounted
                if not d.can_apply_on_discounted:
                    if is_discounted:
                        continue
                if d.amount is not None:
                    r = Money(Decimal(r) - Decimal(d.amount))
                elif d.percent is not None:
                    pourcent = Decimal(d.percent) / Decimal("100")
                    discount = Money(
                        Decimal(product.unit_price) * pourcent)
                    r = r - discount
    return r
