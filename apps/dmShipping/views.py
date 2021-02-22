import json
from django.http import HttpResponse
from .models import ShippingManagement, \
    ShippingAllowed, \
    ShippingCountry, \
    ShippingState, \
    ShippingCity

def get_data(request):

    identifier = request.GET.get('identifier', '')
    if not identifier:
        return HttpResponse(json.dumps({'stat':'failed'}))

    sm = ShippingManagement.objects.filter(identifier=identifier)
    if not sm:
        return HttpResponse(json.dumps({'stat':'failed'}))

    sm = sm[0]

    countries = []
    states = []
    cities = []
    sa = ShippingAllowed.objects.filter(shipping=sm)
    for shipping in sa:
        con = []
        sta = []
        cit = []
        if shipping.countries.all():
            con = list(shipping.countries.all().values_list('name', 'code'))
        else:
            con += []

        if shipping.states.all():
            sta = list(shipping.states.all().values_list('name', 'code'))
        else:
            codes = [ c[1] for c in con]
            sta = list(ShippingState.objects.filter(country__code__in=codes).values_list('name', 'code'))

        if shipping.cities.all():
            cities  += list(shipping.cities.all().values_list('name', 'code'))
        else:
            codes = [ c[1] for c in sta]
            cit = list(ShippingCity.objects.filter(state__code__in=codes).values_list('name', 'code'))

        countries += con
        states += sta
        cities += cit

    data = {
        'countries': countries,
        'states': states,
        'cities': cities,
    }
    return HttpResponse(json.dumps({'stat':' ok', 'data': data}))
