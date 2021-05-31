from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib import admin
from dal import autocomplete
from parler.admin import TranslatableAdmin

from .models import ShippingManagement, ShippingAllowed

#######################################################################
# Shipping Management
#######################################################################


class ShippingAllowedForm(forms.models.ModelForm):

    class Meta:
        model = ShippingAllowed
        fields = ('countries', 'states', 'cities', 'price')
        widgets = {
            'countries': autocomplete.ModelSelect2Multiple(url='country-autocomplete'),
            'states': autocomplete.ModelSelect2Multiple(url='state-autocomplete', forward=['countries']),
            'cities': autocomplete.ModelSelect2Multiple(url='city-autocomplete', forward=['states'])
        }

class ShippingAllowedInline(admin.TabularInline):

    model = ShippingAllowed
    extra = 0
    form = ShippingAllowedForm

@admin.register(ShippingManagement)
class ShippingManagementAdmin(TranslatableAdmin):
    list_display = ["name", "get_price", "identifier", "use_separator"]
    fieldsets = ((None, {
        "fields": [
            "identifier",
            "name_trans",
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
