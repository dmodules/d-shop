from django.contrib import admin

from .models import StripeOrderData

#######################################################################
# Stripe
#######################################################################


@admin.register(StripeOrderData)
class StripeOrderDataAdmin(admin.ModelAdmin):
    list_display = ["order_payment", "receipt_url"]
