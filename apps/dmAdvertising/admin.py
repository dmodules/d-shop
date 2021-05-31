from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from parler.admin import TranslatableAdmin

from .models import dmAdvertisingTopBanner, dmAdvertisingPopup

#######################################################################
# Alerte Publicitaire
#######################################################################


@admin.register(dmAdvertisingTopBanner)
class dmAlertPublicitaireAdmin(TranslatableAdmin):
    list_display = ["text", "link", "get_debut", "get_fin", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["text", "link"]
    fieldsets = [
        (None, {
            "fields": [
                ("text"),
                ("link", "open_blank"),
                ("is_active")
            ]
        }),
        (None, {
            "fields": [
            ]
        }),
        (None, {
            "fields": [
                ("valid_from", "valid_until")
            ]
        })
    ]

    def get_debut(self, obj):
        return obj.valid_from

    get_debut.short_description = _("Start")

    def get_fin(self, obj):
        return obj.valid_until

    get_fin.short_description = _("End")


@admin.register(dmAdvertisingPopup)
class dmAdvertisingPopupAdmin(admin.ModelAdmin):
    list_display = ["__str__", "shown", "get_debut", "get_fin", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["title", "link"]
    readonly_fields = ["shown"]

    def get_debut(self, obj):
        return obj.valid_from

    get_debut.short_description = _("Start")

    def get_fin(self, obj):
        return obj.valid_until

    get_fin.short_description = _("End")
