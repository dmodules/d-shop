from django import template
from django.db.models import Q
import pytz
from datetime import datetime

from boutique.models import Product
from boutique.models import ProductCategory, ProductFilter
from boutique.models import dmAlertPublicitaire

register = template.Library()

@register.simple_tag
def dm_get_products_all():
  result = Product.objects.filter(active=True).order_by('-id')
  return result

@register.simple_tag
def dm_get_category(k):
  result = ProductCategory.objects.get(pk=k)
  return result

@register.simple_tag
def dm_get_category_by_category(k):
  result = ProductCategory.objects.filter(parent_id=k)
  return result

@register.simple_tag
def dm_get_filters_all():
  result = ProductFilter.objects.all()
  return result

@register.simple_tag
def dm_get_all_products(offset,limit):
  offset = int(offset)
  limit = int(limit)
  products = Product.objects.filter(active=True).order_by('id')[offset:offset+limit]
  next_result = Product.objects.filter(active=True).order_by('id')[offset+limit:offset+limit+limit].count()
  result = {
    "products": products,
    "next": next_result
  }
  return result

@register.simple_tag
def dm_get_products_by_category(k,offset,limit):
  offset = int(offset)
  limit = int(limit)
  products = Product.objects.filter(Q(categories=k)|Q(categories__parent=k)|Q(categories__parent__parent=k)|Q(categories__parent__parent__parent=k),active=True).order_by('id')[offset:offset+limit]
  next_result = Product.objects.filter(Q(categories=k)|Q(categories__parent=k)|Q(categories__parent__parent=k)|Q(categories__parent__parent__parent=k),active=True).order_by('id')[offset+limit:offset+limit+limit].count()
  result = {
    "products": products,
    "next": next_result
  }
  return result

@register.simple_tag
def dm_get_products_vedette():
  result = Product.objects.filter(active=True, is_vedette=True).order_by('-id')
  print(result)
  return result

@register.simple_tag
def dm_get_categories_all():
  result = ProductCategory.objects.all()
  return result

@register.simple_tag
def dm_get_categories_parents():
  result = ProductCategory.objects.filter(parent=None)
  return result

@register.simple_tag
def dm_get_nextoffset(k, limit):
  result = int(k) + int(limit)
  return result

@register.simple_tag
def get_alertpublicitaire():
  today = pytz.utc.localize(datetime.utcnow())
  r = dmAlertPublicitaire.objects.filter(Q(is_active=True) & (Q(valid_from__isnull=True) | Q(valid_from__lte=today)) & (Q(valid_until__isnull=True) | Q(valid_until__gt=today))).order_by('?')[:1]
  return r
