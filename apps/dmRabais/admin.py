from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django import forms

from decimal import Decimal

from shop.money import Money
from shop.models.customer import CustomerModel as Customer

from .models import dmRabaisPerCategory
from .models import dmPromoCode
from .models import dmCustomerPromoCode

#######################################################################
# Rabais
#######################################################################


@admin.register(dmRabaisPerCategory)
class dmRabaisPerCategoryAdmin(admin.ModelAdmin):
    fieldsets = [(None, {
        "fields": [
            "name",
            "amount",
            "percent",
            ("is_active", "can_apply_on_discounted"),
            ("valid_from", "valid_until"),
            "categories"
        ]
    })]
    list_display = [
        "name", "get_discount", "is_active", "get_debut", "get_fin"
    ]
    list_filter = ["is_active", "categories"]
    filter_horizontal = ["categories"]
    search_fields = ["name"]

    def get_discount(self, obj):
        if obj.amount is not None:
            return Money(obj.amount)
        elif obj.percent is not None:
            return str(Decimal(obj.percent)) + "%"
        else:
            return "-"

    get_discount.short_description = _("Discount")

    def get_debut(self, obj):
        return obj.valid_from

    get_debut.short_description = _("Start")

    def get_fin(self, obj):
        return obj.valid_until

    get_fin.short_description = _("End")


#######################################################################
# Promo Code
#######################################################################

class CustomerMultipleChoiceField(forms.ModelMultipleChoiceField):
     def label_from_instance(self, obj):
         return str(obj.user.first_name) + " : " + str(obj.user.last_name) + " : " + str(obj.user.email)

@admin.register(dmPromoCode)
class dmPromoCodeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            "fields": [
                "name",
                "code",
                ("is_active", "can_apply_on_discounted"),
                "apply_on_cart",
                "amount",
                "percent"]
        }),
        (_("Limitations"), {
            "fields": [
                ("valid_from", "valid_until"),
                "valid_uses",
                "customer",
                "categories",
                "products"
            ]
        })
    ]
    list_display = ["name", "code", "is_active", "get_debut", "get_fin"]
    list_filter = ["is_active", "categories"]
    filter_horizontal = ["categories", "products"]
    search_fields = ["name"]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "customer":
            return CustomerMultipleChoiceField(queryset=Customer.objects.filter(recognized=2))
        return super(dmPromoCodeAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["code"]
        else:
            return []

    def get_debut(self, obj):
        return obj.valid_from

    get_debut.short_description = _("Start")

    def get_fin(self, obj):
        return obj.valid_until

    get_fin.short_description = _("End")


@admin.register(dmCustomerPromoCode)
class dmCustomerPromoCodeAdmin(admin.ModelAdmin):
    list_display = ["promocode", "customer", "is_expired"]
