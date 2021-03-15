from django.contrib import admin

from .models import dmPortfolio

@admin.register(dmPortfolio)
class dmPortfolioAdmin(admin.ModelAdmin):
    list_display = [
        "title", "active", "image"
    ]
    list_filter = ["active", ]
    search_fields = ["title"]
