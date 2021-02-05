from django import template

from shop.models.defaults.order import Order

register = template.Library()

#######################################################################
# ===---   Simple Tag
#######################################################################

# Admin


@register.simple_tag
def dm_get_order_paymentconfirmed():
    """Get the count of Order with status 'payment_confirmed'"""
    result = Order.objects.filter(
        status="payment_confirmed"
    ).count()
    return result


@register.simple_tag
def dm_get_order_readyfordelivery():
    """Get the count of Order with status 'ready_for_delivery'"""
    result = Order.objects.filter(
        status="ready_for_delivery"
    ).count()
    return result
