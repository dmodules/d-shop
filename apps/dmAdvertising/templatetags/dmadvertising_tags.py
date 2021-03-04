import pytz

from django import template
from django.db.models import Q
from django.utils import timezone

from datetime import datetime

from apps.dmAdvertising.models import dmAdvertisingTopBanner
from apps.dmAdvertising.models import dmAdvertisingPopup

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


@register.simple_tag(takes_context=True)
def get_advertisingpopup(context):
    today = pytz.utc.localize(datetime.utcnow())
    results = dmAdvertisingPopup.objects.filter(
        Q(is_active=True) & (
            Q(valid_from__isnull=True) | Q(valid_from__lte=today)
        ) & (
            Q(valid_until__isnull=True) | Q(valid_until__gt=today)
        )
    ).order_by("?")
    for r in results:
        cookie = context["request"].COOKIES.get("dm_popad_"+str(r.pk), None)
        if r.close_30days and cookie is not None:
            results = results.exclude(pk=r.pk)
    result = results[:1]
    for r in result:
        r.shown = r.shown + 1
        r.save()
    return result
