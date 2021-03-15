from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from .models import dmJobDescription
from .models import dmJobApplication

@admin.register(dmJobDescription)
class dmJobDescriptionAdmin(admin.ModelAdmin):
    list_display = [
        "title", "slug", "is_active", "created_at"
    ]
    readonly_fields  = ['slug', ]
    list_filter = ["is_active", ]
    search_fields = ["title"]

@admin.register(dmJobApplication)
class dmJobApplicationAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "job", 'document',]
    search_fields = ["name"]
