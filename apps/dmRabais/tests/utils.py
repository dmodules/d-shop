
import pytz
from datetime import datetime, timedelta

from dshop.tests.utils import category
from apps.dmRabais.models import \
    dmRabaisPerCategory, \
    dmPromoCode

def create_discount(data=None):
    data = {
        'name': 'Test Discount',
        'discount_type': 1,
        'amount': 10,
        'is_active': True,
        'valid_from': pytz.utc.localize(datetime.today() - timedelta(days=2)),
        'valid_until': pytz.utc.localize(datetime.today() + timedelta(days=3)),
    }
    try:
        drpc = dmRabaisPerCategory.objects.create(**data)
        cat = category()
        drpc.categories.add(cat)
    except Exception as e:
        print(e)
        return False
    return True

def create_promo(data=None):
    data = {
        'name': 'Test Promo',
        'code': 'TEST50',
        'discount_type': 1,
        'amount': 10,
        'is_active': True,
        'valid_from': pytz.utc.localize(datetime.today()),
        'valid_until': pytz.utc.localize(datetime.today()),
    }

    try:
        dmpc = dmPromoCode.objects.create(**data)
        cat = category()
        dmpc.categories.add(cat)
    except Exception as e:
        print(e)
        return False
    return True
