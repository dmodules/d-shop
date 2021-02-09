from django.contrib import admin

from .models import dmStockLog

@admin.register(dmStockLog)
class dmStockLogAdmin(admin.ModelAdmin):
    fieldsets = [(None, {
        "fields": [
            "product_name",
            ("product_square_code", "variant_square_code"),
            ("old_quantity", "new_quantity"),
            ("stock_update_date", "update_from"),
        ]
    })]
    list_display = [
        "product_name", "old_quantity", "new_quantity", "update_from", "stock_update_date"
    ]
    readonly_fields = [
        "product_name",
        "product_square_code",
        "variant_square_code",
        "old_quantity",
        "new_quantity",
        "stock_update_date",
        "update_from"
    ]
    list_filter = ["update_from"]
    search_fields = ["product_name", "product_square_code", "variant_square_code"]
