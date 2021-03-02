from django.contrib import admin
from django.utils.translation import pgettext_lazy
from django.urls import reverse, NoReverseMatch
from django.utils.html import format_html

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
            "get_customer_link",
            "status",
            ("created_at", "updated_at"),
        ]
    })]
    readonly_fields = ['created_at', 'updated_at', 'get_customer_link']
    inlines = [dmQuotationItemInline]
    list_display = [
        "number", "customer", "status", "created_at", "updated_at"
    ]

    def get_customer_link(self, obj):
        try:
            url = reverse('admin:shop_customerproxy_change', args=(obj.customer.pk,))
            return format_html('<a href="{0}" target="_new">{1}</a>', url, obj.customer.get_username())
        except NoReverseMatch:
            return format_html('<strong>{0}</strong>', obj.customer.get_username())
    get_customer_link.short_description = pgettext_lazy('admin', "Customer")
