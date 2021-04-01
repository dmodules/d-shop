import json
from django.db.models import Q
from django.http import HttpResponse
from .models import ShippingManagement, ShippingAllowed
from cities_light.models import Country, Region, City
from dal import autocomplete

class CountryAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Country.objects.none()

        qs = Country.objects.all()

        if self.q:
            qs = qs.filter(Q(name__istartswith=self.q))
        return qs


class StateAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Region.objects.none()

        countries = self.forwarded.get('countries', None)
        qs = Region.objects.all()

        if countries:
            qs = qs.filter(country__id__in=countries)

        if self.q:
            qs = qs.filter(Q(name__istartswith=self.q) | Q(country__name__istartswith=self.q))
        return qs


class CityAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return City.objects.none()

        states = self.forwarded.get('states', None)
        qs = City.objects.all()

        if states:
            qs = qs.filter(region_id__in=states)

        if self.q:
            qs = qs.filter(Q(name__istartswith=self.q) | Q(region__name__istartswith=self.q))
        return qs

def get_data(request):  # noqa: C901

    identifier = request.GET.get("identifier", "")
    if not identifier:
        return HttpResponse(json.dumps({"valid": False}))

    sm = ShippingManagement.objects.filter(identifier=identifier)
    if not sm:
        return HttpResponse(json.dumps({"valid": False}))

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
            con = list(shipping.countries.all().values_list("name", "code2"))
        else:
            con += []

        if shipping.states.all():
            sta = list(shipping.states.all().values_list("name", "slug"))
            if not con:
                for s in sta:
                    s_obj = Region.objects.get(slug=s[1])
                    con += [(s_obj.country.name, s_obj.country.code2)]
        else:
            codes = [c[1] for c in con]
            sta = list(Region.objects.filter(country__code2__in=codes).values_list("name", "slug"))

        if shipping.cities.all():
            s_slug = [ s[1] for s in sta ]
            cities += list(shipping.cities.exclude(region__slug__in=s_slug).values_list("name", "id"))
            if not sta:
                city_id = [ c[1] for c in cities ]
                city_obj = City.objects.filter(id__in=city_id)
                for c_obj in city_obj:
                    tpl = (c_obj.region.name, c_obj.region.slug)
                    if tpl not in sta:
                        sta.append(tpl)
            if not con:
                for s in sta:
                    s_obj = Region.objects.get(slug=s[1])
                    con += [(s_obj.country.name, s_obj.country.code2)]
        else:
            codes = [c[1] for c in sta]
            cit = list(City.objects.filter(region__slug__in=codes).values_list('name', 'id'))

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
            st = Region.objects.filter(slug=s[1], country__code2=country).first()
            if st:
                if st.slug not in temp:
                    temp[st.slug] = st.name
        temp_st[country] = temp

    temp_ct = {}
    processed = []
    for state in states:
        temp = {}
        if state[1] in processed:
            continue
        processed.append(state[1])
        city_id = [ c[1] for c in cities ]
        city_obj = City.objects.filter(id__in=city_id, region__slug=state[1])
        for c in city_obj:
            if c.id not in temp:
                temp[c.id] = c.name
        
        temp_ct[state[1]] = temp

    data = {
        'countries': temp_co,
        'states': temp_st,
        'cities': temp_ct,
    }
    return HttpResponse(json.dumps({"valid": True, "datas": data}))
