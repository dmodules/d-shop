

from .models import ShippingManagement, ShippingAllowed


def get_price(identifier, country, state, city):

    sm = ShippingManagement.objects.get(identifier=identifier)
    #Filter by Shipping Identifier
    sa = ShippingAllowed.objects.filter(shipping=sm)
    #Filter by country
    sa = sa.filter(countries__code=country)

    if sa.count() == 1:
        return sa[0].price
    else:
        sa = sa.filter(states__code=state)
        if not sa:
            return 0
        if sa.count() == 1:
            return sa[0].price
        else:
            sa = sa.filter(cities__code=city)
            if not sa:
                return 0
            else:
                return sa[0].price
    
