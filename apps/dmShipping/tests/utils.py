
from apps.dmShipping.models import ShippingManagement


def create_shipping(data=None):
    data = {
        'name': 'Shipping Method',
        'identifier': 'standard-shipping',
        'price': 10,
        'separator': 150,
        'price_after': 5,
    }
    try:
        ds = ShippingManagement.objects.create(**data)
    except Exception as e:
        print(e)
        return False
    return ds
