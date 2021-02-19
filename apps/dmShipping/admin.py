from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from .models import ShippingManagement, \
    ShippingCountry, \
    ShippingAllowed, \
    ShippingState, \
    ShippingCity

#######################################################################
# Shipping Management
#######################################################################


class ShippingAllowedInline(admin.TabularInline):

    model = ShippingAllowed
    extra = 0

@admin.register(ShippingManagement)
class ShippingManagementAdmin(admin.ModelAdmin):
    list_display = ["name", "get_price", "identifier", "use_separator"]
    fieldsets = ((None, {
        "fields": [
            "identifier",
            "name",
            "price",
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
