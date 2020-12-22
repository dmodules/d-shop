from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from .models import ThemeManagement

#######################################################################
# Theme Management
#######################################################################


@admin.register(ThemeManagement)
class ThemeManagementAdmin(admin.ModelAdmin):
    list_display = ['theme', 'active', ]