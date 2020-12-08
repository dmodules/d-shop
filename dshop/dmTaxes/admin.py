from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from .models import CanadaTaxManagement

#######################################################################
# Canada Tax Management
#######################################################################

@admin.register(CanadaTaxManagement)
class CanadaTaxManagementAdmin(admin.ModelAdmin):
  list_display = ['state', 'hst', 'gst', 'pst', 'qst']