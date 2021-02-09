from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from .models import dmQuotation, dmQuotationItem


class dmQuotationItemInline(admin.TabularInline):

    model = dmQuotationItem
    extra = 0

@admin.register(dmQuotation)
class dmQuotationAdmin(admin.ModelAdmin):
    fieldsets = [(None, {
        "fields": [
            "number",
            "status",
            ("created_at", "updated_at"),
        ]
    })]
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ dmQuotationItemInline ]
    list_display = [
        "number", "status", "created_at", "updated_at"
    ]
