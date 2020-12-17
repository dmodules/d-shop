from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from decimal import Decimal

from shop.money import Money

from .models import dmRabaisPerCategory

#######################################################################
# Rabais
#######################################################################

@admin.register(dmRabaisPerCategory)
class dmRabaisPerCategoryAdmin(admin.ModelAdmin):
  verbose_name = _("Rabais")
  verbose_name_plural = _("Rabais")
  fieldsets = [
    (None, {
      "fields": [
        "name",
        "amount",
        "percent",
        "is_active",
        ("valid_from", "valid_until"),
        "categories"
      ]
    })
  ]
  list_display = ["name", "get_discount", "is_active", "get_debut", "get_fin"]
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
  get_discount.short_description = _("Rabais")

  def get_debut(self, obj):
    return obj.valid_from
  get_debut.short_description = _("Début")

  def get_fin(self, obj):
    return obj.valid_until
  get_fin.short_description = _("Fin")