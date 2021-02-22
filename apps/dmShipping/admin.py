from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib import admin
from dal import autocomplete

from .models import ShippingManagement, \
    ShippingCountry, \
    ShippingAllowed, \
    ShippingState, \
    ShippingCity

#######################################################################
# Shipping Management
#######################################################################


class ShippingAllowedForm(forms.models.ModelForm):

    class Meta:
        model = ShippingAllowed
        fields = ('countries', 'states', 'cities', 'price')
        widgets = {
            'countries': autocomplete.ModelSelect2Multiple(url='country-autocomplete'),
            'states': autocomplete.ModelSelect2Multiple(url='state-autocomplete',forward=['countries']),
            'cities': autocomplete.ModelSelect2Multiple(url='city-autocomplete', forward=['states'])
        }

class ShippingAllowedInline(admin.TabularInline):

    model = ShippingAllowed
    extra = 0
    form = ShippingAllowedForm

@admin.register(ShippingManagement)
class ShippingManagementAdmin(admin.ModelAdmin):
    list_display = ["name", "get_price", "identifier", "use_separator"]
    fieldsets = ((None, {
        "fields": [
            "identifier",
            "name",
            "price",
            "taxed_shipping"
        ],
    }), (_("Create a discount on shipping"), {
        "fields": [
            "use_separator",
            "separator",
            "price_after"
        ],
    }))

    inlines = [ShippingAllowedInline]


class ShippingStateInline(admin.TabularInline):

    model = ShippingState
    extra = 0

class ShippingCityInline(admin.TabularInline):

    model = ShippingCity
    extra = 0

@admin.register(ShippingCountry)
class ShippingCountryAdmin(admin.ModelAdmin):

    list_display = ["name", "code", "total_state"]
    inlines = [ShippingStateInline]

    def total_state(self, obj):
        return ShippingState.objects.filter(country=obj).count()

@admin.register(ShippingState)
class ShippingStateAdmin(admin.ModelAdmin):

    list_display = ["country", "name", "code", "total_city"]
    inlines = [ShippingCityInline]

    def total_city(self, obj):
        return ShippingCity.objects.filter(state=obj).count()
