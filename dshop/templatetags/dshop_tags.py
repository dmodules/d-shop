import re

from datetime import datetime

from django import template
from django.conf import settings
from django.db.models import Q

from dshop.models import dmSite
from dshop.models import Product
from dshop.models import ProductCategory, ProductFilter, ProductBrand
from dshop.utils import get_coords_from_address

from feature_settings import *

register = template.Library()

#######################################################################
# ===---   Filters
#######################################################################


@register.filter
def ts_to_str(timestamp):
    """Timestamp to string"""
    if timestamp.endswith("-05:00"):
        ts = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f-05:00")
    elif timestamp.endswith("-04:00"):
        ts = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f-04:00")
    else:
        ts = timestamp
    return ts


@register.filter
def phone_canadian(string):
    """Remove all but digits from string and make it canadian phone"""
    return "+1" + re.sub(r"\D", "", string)

#######################################################################
# ===---   Simple Tag
#######################################################################

# Site


@register.simple_tag
def get_setting(name):
    """Get the value of a setting from key name"""
    return getattr(settings, name, "")


@register.simple_tag
def dm_get_logos():
    """Get logos from the first Site registered in admin panel"""
    result = dmSite.objects.first()
    if not result:
        return []
    return result.logos.first()


@register.simple_tag
def dm_get_site_contacts():
    """Get contacts's data from the first Site registered in admin panel"""
    result = dmSite.objects.first()
    if not result:
        return []
    return result.contacts.first()


@register.simple_tag
def dm_get_site_coord():
    """Get coordinates's data from Site's address"""
    coords = {
        "lat": "",
        "lon": ""
    }
    try:
        result = dmSite.objects.first()
        contacts = result.contacts.first()
        address = str(contacts.address)
        location = get_coords_from_address(address)
        if location:
            coords = {
                "lat": str(location.latitude).replace(",", "."),
                "lon": str(location.longitude).replace(",", ".")
            }
    except Exception:
        pass
    return coords


@register.simple_tag
def dm_get_site_socials():
    """Get socials's data from the first Site registered in admin panel"""
    result = dmSite.objects.first()
    if not result:
        return []
    return result.social.all()


@register.simple_tag
def dm_get_site_termsandconditions():
    """Get Terms and Conditions's text from the first Site registered in admin panel"""
    result = dmSite.objects.first()
    return result.termsandconditions.first()


# Shop


@register.simple_tag
def dm_get_attributes_list(k):
    """Make a list from variant attribute"""
    result = []
    for a in k.attribute.all():
        result.append(a.value)
    return result


@register.simple_tag
def dm_get_products_all():
    """Get data from all active products"""
    result = Product.objects.filter(active=True, categories__active=True).order_by('-id')
    return result


@register.simple_tag
def dm_get_category(k):
    """Get category's data from pk/id key"""
    result = ProductCategory.objects.get(pk=k)
    return result


@register.simple_tag
def dm_get_categories_parents():
    """Get all categories that is not a child of another category"""
    result = ProductCategory.objects.filter(parent=None, active=True)
    return result


@register.simple_tag
def dm_get_category_by_category(k):
    """Get category's data from parent pk/id key"""
    result = ProductCategory.objects.filter(parent_id=k, active=True)
    return result


@register.simple_tag
def dm_get_filters_all():
    """Get data from all filters"""
    result = ProductFilter.objects.all()
    return result


@register.simple_tag
def dm_get_brands_all():
    """Get data from all brands"""
    result = ProductBrand.objects.all()
    return result


@register.simple_tag
def dm_get_brand(k):
    """Get brand's data from pk/id key"""
    result = ProductBrand.objects.get(pk=k)
    return result


@register.simple_tag
def dm_get_all_products(offset, limit):
    """Get data from all products with offset and limit"""
    offset = int(offset)
    limit = int(limit)
    products = Product.objects.filter(
        Q(categories__active=True) | Q(categories=None),
        active=True
    ).order_by('id').distinct()[offset:offset+limit]
    next_result = Product.objects.filter(
        Q(categories__active=True) | Q(categories=None),
        active=True
    ).distinct().order_by('id')[offset+limit:offset+limit+limit].count()
    result = {
        "products": products,
        "next": next_result
    }
    return result


@register.simple_tag
def dm_get_products_by_category(k, offset, limit):
    """Get data from all products from category's pk/id key with offset and limit"""
    offset = int(offset)
    limit = int(limit)
    products = Product.objects.filter(Q(categories=k) | Q(categories__parent=k) | Q(categories__parent__parent=k) | Q(
        categories__parent__parent__parent=k), active=True).distinct()

    # Filter product for categories = True
    products = products.filter(categories__active=True)[offset:offset+limit]
    next_result = Product.objects.filter(
        Q(categories=k) | Q(categories__parent=k) | Q(categories__parent__parent=k) | Q(
            categories__parent__parent__parent=k
        ), active=True
    ).distinct()[offset+limit:offset+limit+limit].count()
    result = {
        "products": products,
        "next": next_result
    }
    return result


@register.simple_tag
def dm_get_products_by_brand(k, offset, limit):
    """Get data from all products from brand's pk/id key with offset and limit"""
    offset = int(offset)
    limit = int(limit)
    products = Product.objects.filter(
        brand=k, active=True
    ).order_by('id')[offset:offset+limit]
    next_result = Product.objects.filter(
        brand=k, active=True
    ).order_by('id')[offset+limit:offset+limit+limit].count()
    result = {
        "products": products,
        "next": next_result
    }
    return result


@register.simple_tag
def dm_get_products_related(categories, id):
    """Get data from all product from categories but the specified product by pk/id key"""
    products = Product.objects.none()
    for k in categories.all():
        products = products | Product.objects.filter(
            Q(categories=k) | Q(categories__parent=k) | Q(
                categories__parent__parent=k
            ) | Q(categories__parent__parent__parent=k), active=True
        ).exclude(pk=id).distinct()
        if products.count() < 4 and k.parent is not None:
            products = products | Product.objects.filter(
                Q(categories=k.parent) | Q(categories__parent=k.parent) | Q(
                    categories__parent__parent=k.parent
                ) | Q(categories__parent__parent__parent=k.parent), active=True
            ).exclude(pk=id).exclude(pk__in=products).distinct()
        if products.count() < 4 and k.parent and k.parent.parent is not None:
            products = products | Product.objects.filter(
                Q(categories=k.parent.parent) | Q(categories__parent=k.parent.parent) | Q(
                    categories__parent__parent=k.parent.parent
                ) | Q(categories__parent__parent__parent=k.parent.parent), active=True
            ).exclude(pk=id).exclude(pk__in=products).distinct()
    result = {
        "products": products[:4]
    }
    return result


@register.simple_tag
def dm_get_products_vedette():
    """Get data from all active and featured products"""
    result = Product.objects.filter(
        active=True, is_vedette=True).order_by('-id')
    return result


@register.simple_tag
def dm_variants_is_outofstock(k):
    """Check if all variants is out of stock"""
    result = True
    for variant in k.all():
        if variant.quantity > 0:
            result = False
    return result


@register.simple_tag
def dm_variants_is_discounted(k):
    """Check if a variant is discounted in a list of variants"""
    result = False
    for variant in k.all():
        if variant.is_discounted:
            result = True
    return result


@register.simple_tag
def dm_quotation_feature():
    QUOTATION = False
    try:
        QUOTATION = QUOTATION_FEATURE
    except Exception:
        pass
    if QUOTATION:
        return True
    return False
