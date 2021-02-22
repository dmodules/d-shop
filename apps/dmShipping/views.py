import json
from django.db.models import Q
from django.http import HttpResponse
from .models import ShippingManagement, \
    ShippingAllowed, \
    ShippingCountry, \
    ShippingState, \
    ShippingCity
from dal import autocomplete

class CountryAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ShippingCountry.objects.none()

        qs = ShippingCountry.objects.all()

        if self.q:
            qs = qs.filter(Q(name__istartswith=self.q))
        return qs


class StateAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ShippingState.objects.none()

        countries = self.forwarded.get('countries', None)
        qs = ShippingState.objects.all()

        if countries:
            qs = qs.filter(country__id__in=countries)

        if self.q:
            qs = qs.filter(Q(name__istartswith=self.q) | Q(country__name__istartswith=self.q))
        return qs


class CityAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ShippingCity.objects.none()

        states = self.forwarded.get('states', None)
        qs = ShippingCity.objects.all()

        if states:
            qs = qs.filter(state__id__in=states)

        if self.q:
            qs = qs.filter(Q(name__istartswith=self.q) | Q(state__name__istartswith=self.q))
        return qs


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
            if not con:
                for s in sta:
                    s_obj = ShippingState.objects.get(code=s[1])
                    con += [(s_obj.country.name, s_obj.country.code)]
        else:
            codes = [ c[1] for c in con]
            sta = list(ShippingState.objects.filter(country__code__in=codes).values_list('name', 'code'))

        if shipping.cities.all():
            cities  += list(shipping.cities.all().values_list('name', 'code'))
            if not sta:
                for c in cities:
                    c_obj = ShippingCity.objects.get(code=c[1])
                    sta += [(c_obj.state.name, c_obj.state.code)]
            if not con:
                for s in sta:
                    s_obj = ShippingState.objects.get(code=s[1])
                    con += [(s_obj.country.name, s_obj.country.code)]
        else:
            codes = [ c[1] for c in sta]
            cit = list(ShippingCity.objects.filter(state__code__in=codes).values_list('name', 'code'))

        countries += con
        states += sta
        cities += cit

    temp_co = {}
    for c in countries:
        if c[1] not in temp_co:
            temp_co[c[1]] = c[0]

    temp_st = {}
    for country in temp_co:
        temp = {}
        for s in states:
            st = ShippingState.objects.filter(code=s[1], country__code=country).first()
            if st:
                if st.code not in temp:
                    temp[st.code] = st.name
        temp_st[country] = temp

    temp_ct = {}
    for state in states:
        temp = {}
        for c in cities:
            ct = ShippingCity.objects.filter(code=c[1], state__code=state[1]).first()
            if ct:
                if ct.code not in temp:
                    temp[ct.code] = ct.name
        temp_ct[state[1]] = temp

    data = {
        'countries': temp_co,
        'states': temp_st,
        'cities': temp_ct,
    }
    return HttpResponse(json.dumps({'stat':' ok', 'data': data}))
