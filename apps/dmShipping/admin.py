from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from .models import ShippingManagement

#######################################################################
# Shipping Management
#######################################################################

@admin.register(ShippingManagement)
class ShippingManagementAdmin(admin.ModelAdmin):
  list_display = ["name", "get_price", "identifier"]
