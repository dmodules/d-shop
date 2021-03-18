from django import template

from apps.dmJobModule.models import dmJobDescription

register = template.Library()


@register.simple_tag
def dmjob_get_lastjob(x):
    """Get the last x job offers"""
    result = dmJobDescription.objects.all()[:x]
    return result
