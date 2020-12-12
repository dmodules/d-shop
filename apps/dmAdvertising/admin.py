from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from .models import dmAdvertisingTopBanner

#######################################################################
# Alerte Publicitaire
#######################################################################

@admin.register(dmAdvertisingTopBanner)
class dmAlertPublicitaireAdmin(admin.ModelAdmin):
  list_display = ["text", "link", "get_debut", "get_fin", "is_active"]
  list_filter = ["is_active"]
  search_fields = ["text", "link"]

  def get_debut(self, obj):
    return obj.valid_from
  get_debut.short_description = _("Début")

  def get_fin(self, obj):
    return obj.valid_until
  get_fin.short_description = _("Fin")
