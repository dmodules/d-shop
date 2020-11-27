from django import template
from django.conf import settings
import datetime
import re

register = template.Library()

@register.simple_tag
def get_setting(name):
  return getattr(settings, name, "")

@register.filter
def ts_to_str(timestamp):
  ts = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
  return ts

@register.filter
def makephone(string):
  return "+1" + re.sub("\D", "", string)
