from django.conf.urls import url

from .views import get_data, \
    CountryAutocomplete, \
    StateAutocomplete, \
    CityAutocomplete

urlpatterns = [
    url(r'^get-data/', get_data),
    url(r'^country-autocomplete/$', CountryAutocomplete.as_view(), name='country-autocomplete'),
    url(r'^state-autocomplete/$', StateAutocomplete.as_view(), name='state-autocomplete'),
    url(r'^city-autocomplete/$', CityAutocomplete.as_view(), name='city-autocomplete'),

]
