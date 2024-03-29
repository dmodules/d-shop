import os

from django import template
from django.apps import apps

from datetime import datetime

from settings import path_to_extended

from shop.money import Money
from shop.models.defaults.order import Order

from dshop.models import Product, ProductDefault, ProductVariable

register = template.Library()

#######################################################################
# ===---   Simple Tag
#######################################################################

# Admin


@register.simple_tag
def dm_get_extended_apps():
    result = []
    if os.path.exists(path_to_extended):
        for item in os.listdir(path_to_extended):
            for a in apps.get_app_configs():
                if a.name == "extended_apps."+item:
                    aa = []
                    for m in a.get_models():
                        aa.append({
                            "name": str(m._meta.verbose_name.title()),
                            "label": str(m.__name__),
                            "link": m._meta.model_name
                        })
                    result.append(
                        {
                            "name": str(a.verbose_name),
                            "label": str(item),
                            "apps": aa
                        }
                    )
    return result


@register.simple_tag
def dm_get_order_sells():
    """Get the data about this month sells"""
    result = {}
    # ===--- this month
    thismonth_amount = Money(0)
    thismonth_quantity = 0
    thismonth_month = datetime.now().month
    thismonth_year = datetime.now().year
    for o in Order.objects.filter(
        created_at__year=thismonth_year,
        created_at__month=thismonth_month
    ):
        thismonth_amount += o.total
        thismonth_quantity += 1
    # ===--- last month
    lastmonth = datetime.now().replace(day=1)
    if lastmonth.month > 1:
        lastmonth = lastmonth.replace(month=lastmonth.month - 1)
    else:
        lastmonth = lastmonth.replace(month=12)
        lastmonth = lastmonth.replace(year=lastmonth.year - 1)
    lastmonth_amount = Money(0)
    lastmonth_quantity = 0
    lastmonth_month = lastmonth.month
    lastmonth_year = lastmonth.year
    for o in Order.objects.filter(
        created_at__year=lastmonth.year,
        created_at__month=lastmonth.month
    ):
        lastmonth_amount += o.total
        lastmonth_quantity += 1
    # ===---
    result = {
        "thismonth": {
            "month": thismonth_month,
            "year": thismonth_year,
            "amount": thismonth_amount,
            "quantity": thismonth_quantity
        },
        "lastmonth": {
            "month": lastmonth_month,
            "year": lastmonth_year,
            "amount": lastmonth_amount,
            "quantity": lastmonth_quantity
        }
    }
    return result


@register.simple_tag
def dm_get_order_status():
    """Get the count of Order with sepcific status"""
    result = {}
    order_paymentconfirmed = 0
    order_readyfordelivery = 0
    # ===---
    order_paymentconfirmed = Order.objects.filter(
        status="payment_confirmed"
    ).count()
    order_readyfordelivery = Order.objects.filter(
        status="ready_for_delivery"
    ).count()
    # ===---
    result = {
        "paymentconfirmed": order_paymentconfirmed,
        "readyfordelivery": order_readyfordelivery
    }
    return result


@register.simple_tag
def dm_get_products_stocks():
    """Get the low and out of stock counts from Products"""
    result = {}
    outofstock = 0
    lowonstock = 0
    # ===--- out of stock count
    for p in Product.objects.all():
        if type(p) == ProductDefault:
            if p.quantity <= 0:
                outofstock += 1
            elif p.quantity <= 3:
                lowonstock += 1
        elif type(p) == ProductVariable:
            for v in p.variants.all():
                if v.quantity <= 0:
                    outofstock += 1
                elif v.quantity <= 3:
                    lowonstock += 1
    # ===---
    result = {
        "outofstock": outofstock,
        "lowonstock": lowonstock
    }
    return result


@register.simple_tag
def dm_get_order_bestsellers():
    """Get the data about the 5 best selled products of this month"""
    result = {}
    bestseller_products = []
    bestseller_quantity = 0
    all_selled = []
    for o in Order.objects.filter(
        created_at__year=datetime.now().year,
        created_at__month=datetime.now().month
    ):
        for item in o.items.all():
            already = False
            for x in all_selled:
                if x["name"] == str(item):
                    x["quantity"] += item.quantity
                    already = True
            if not already:
                all_selled.append({
                    "name": str(item),
                    "quantity": item.quantity
                })
    bestseller_products = sorted(
        all_selled,
        key=lambda h: (int(h["quantity"])),
        reverse=True
    )[:5]
    # ===---
    result = {
        "products": bestseller_products,
        "quantity": bestseller_quantity
    }
    return result
