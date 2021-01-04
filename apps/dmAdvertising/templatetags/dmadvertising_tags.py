import pytz

from django import template
from django.db.models import Q

from datetime import datetime

from apps.dmAdvertising.models import dmAdvertisingTopBanner

register = template.Library()

#######################################################################
# Alerte Publicitaire
#######################################################################

@register.simple_tag
def get_advertisingtopbanner():
    today = pytz.utc.localize(datetime.utcnow())
    r = dmAdvertisingTopBanner.objects.filter(
        Q(is_active=True) & (
            Q(valid_from__isnull=True) | Q(valid_from__lte=today)
        ) & (
            Q(valid_until__isnull=True) | Q(valid_until__gt=today)
        )
    ).order_by("?")[:1]
    return r
