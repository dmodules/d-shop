from django import template

from apps.dmTheme.models import dmTheme

register = template.Library()

#######################################################################
# ===---   Simple Tag
#######################################################################


@register.simple_tag
def dm_get_theme():
    result = dmTheme.objects.first()
    return result
