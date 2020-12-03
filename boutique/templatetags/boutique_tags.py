from django import template
from django.db.models import Q

import re
import json
import pytz
from datetime import datetime
from shop.money import Money
from decimal import Decimal

from boutique.models import Product
from boutique.models import ProductVariableVariant
from boutique.models import ProductCategory, ProductFilter
from boutique.models import dmRabaisPerCategory
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
def dm_get_products_related(categories, id):
  products = Product.objects.none()
  for k in categories.all():
    products = products | Product.objects.filter(Q(categories=k)|Q(categories__parent=k)|Q(categories__parent__parent=k)|Q(categories__parent__parent__parent=k),active=True).exclude(pk=id).order_by('id')[:4]
  result = {
    "products": products
  }
  return result

@register.simple_tag
def dm_get_products_vedette():
  result = Product.objects.filter(active=True, is_vedette=True).order_by('-id')
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

# Alerts publicitaires

@register.simple_tag
def get_alertpublicitaire():
  today = pytz.utc.localize(datetime.utcnow())
  r = dmAlertPublicitaire.objects.filter(Q(is_active=True) & (Q(valid_from__isnull=True) | Q(valid_from__lte=today)) & (Q(valid_until__isnull=True) | Q(valid_until__gt=today))).order_by('?')[:1]
  return r

# Rabais

@register.simple_tag
def product_discount_price(id):
  p = Product.objects.get(pk=id)
  today = pytz.utc.localize(datetime.utcnow())
  all_discounts = dmRabaisPerCategory.objects.filter(Q(categories__in=p.categories.all()) & Q(is_active=True) & (Q(valid_from__isnull=True) | Q(valid_from__lte=today)) & (Q(valid_until__isnull=True) | Q(valid_until__gt=today)))
  if all_discounts.count() > 0:
    r = p.unit_price
    for d in all_discounts:
      if d.amount is not None:
        r = Money(Decimal(r) - Decimal(d.amount))
      elif d.percent is not None:
        pourcent = Decimal(d.percent) / Decimal('100')
        discount = Money(Decimal(p.unit_price) * pourcent)
        r = r - discount
  else:
    r = p.unit_price
  if Decimal(r) < 0:
    r = Money(0)
  return r

@register.simple_tag
def product_variant_discount_price(id):
  p = ProductVariableVariant.objects.get(pk=id)
  today = pytz.utc.localize(datetime.utcnow())
  all_discounts = dmRabaisPerCategory.objects.filter(Q(categories__in=p.product.categories.all()) & Q(is_active=True) & (Q(valid_from__isnull=True) | Q(valid_from__lte=today)) & (Q(valid_until__isnull=True) | Q(valid_until__gt=today)))
  if all_discounts.count() > 0:
    r = p.unit_price
    for d in all_discounts:
      if d.amount is not None:
        r = Money(Decimal(r) - Decimal(d.amount))
      elif d.percent is not None:
        pourcent = Decimal(d.percent) / Decimal('100')
        discount = Money(Decimal(p.unit_price) * pourcent)
        r = r - discount
  else:
    r = p.unit_price
  if Decimal(r) < 0:
    r = Money(0)
  return r

@register.simple_tag
def product_discounts(id):
  p = Product.objects.get(pk=id)
  today = pytz.utc.localize(datetime.utcnow())
  all_discounts = dmRabaisPerCategory.objects.filter(Q(categories__in=p.categories.all()) & Q(is_active=True) & (Q(valid_from__isnull=True) | Q(valid_from__lte=today)) & (Q(valid_until__isnull=True) | Q(valid_until__gt=today)))
  if all_discounts.count() > 0:
    return all_discounts
  else:
    return None

@register.simple_tag
def product_undiscount_price(id, price):
  p = Product.objects.get(pk=id)
  current = re.search(r"[-+]?(\d+([.,]\d*)?|[.,]\d+)([eE][-+]?\d+)?", str(price)).group()
  original = re.search(r"[-+]?(\d+([.,]\d*)?|[.,]\d+)([eE][-+]?\d+)?", str(p.unit_price)).group()
  if original != current:
    return p.unit_price
  else:
    return None