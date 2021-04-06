

from .models import ShippingManagement, ShippingAllowed


def get_price(identifier, country, state, city):

    sm = ShippingManagement.objects.get(identifier=identifier)
    # Filter by Shipping Identifier
    sa = ShippingAllowed.objects.filter(shipping=sm)
    if not sa:
        return sm.price
    # Filter by country
    sa = sa.filter(countries__code2=country)
    if not sa:
        sa = ShippingAllowed.objects.filter(shipping=sm)
        sa = sa.filter(states__name=state)
    if not sa:
        sa = ShippingAllowed.objects.filter(shipping=sm)
        sa = sa.filter(cities__name=city)

    if sa.count() == 1:
        return sa[0].price
    else:
        sa = sa.filter(states__name=state)
        if not sa:
            return 0
        if sa.count() == 1:
            return sa[0].price
        else:
            sa = sa.filter(cities__name=city)
            if not sa:
                return 0
            else:
                return sa[0].price
