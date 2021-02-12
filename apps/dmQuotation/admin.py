from django.contrib import admin

from .models import dmQuotation, dmQuotationItem


class dmQuotationItemInline(admin.TabularInline):

    model = dmQuotationItem
    fields = ('product_name', 'product_code_c', 'variant_attribute', 'quantity', 'unit_price',)
    readonly_fields = ('product_name', 'product_code_c', 'variant_attribute', 'quantity',)
    extra = 0

    def product_code_c(self, obj):
        if obj.product_type == 1:
            return obj.product_code
        else:
            return obj.variant_code
    product_code_c.short_description = 'Product Code'

@admin.register(dmQuotation)
class dmQuotationAdmin(admin.ModelAdmin):
    fieldsets = [(None, {
        "fields": [
            "number",
            "customer",
            "status",
            ("created_at", "updated_at"),
        ]
    })]
    readonly_fields = ['created_at', 'updated_at']
    inlines = [dmQuotationItemInline]
    list_display = [
        "number", "customer", "status", "created_at", "updated_at"
    ]
