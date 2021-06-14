
import pytz
from datetime import datetime, timedelta

from apps.dmAdvertising.models import dmAdvertisingTopBanner


def create_advertise_top_banner(data=None):
    data = {
        'text': 'Top Banner',
        'link': 'https://www.google.com',
        'open_blank': True,
        'is_active': True,
        'valid_from': pytz.utc.localize(datetime.today() - timedelta(days=2)),
        'valid_until': pytz.utc.localize(datetime.today() + timedelta(days=3)),
    }
    try:
        dma = dmAdvertisingTopBanner.objects.create(**data)
    except Exception as e:
        print(e)
        return False
    return dma
