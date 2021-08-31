from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from .models import dmTheme


@admin.register(dmTheme)
class dmThemeAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    search_fields = ["name"]
    fieldsets = [
        (None, {
            "fields": [
                ("name"),
                ("is_active")
            ]
        }),
        (_("Base"), {
            "fields": [
                ("bg_base"),
                ("txt_base"),
                ("lnk_base"),
                ("hov_base")
            ]
        }),
        (_("Default Button"), {
            "fields": [
                "rad_button",
                "txt_button",
                "bor_button",
                "bg_button",
                "txt_hov_button",
                "bor_hov_button",
                "bg_hov_button"
            ],
            "classes": ["collapse"]
        }),
        (_("Default Input"), {
            "fields": [
                "rad_input",
                "bg_input",
                "bor_input",
                "txt_input"
            ],
            "classes": ["collapse"]
        }),
        (_("Default Checkbox"), {
            "fields": [
                "rad_checkbox",
                "bco_checkbox",
                "act_checkbox",
                "act_chk_checkbox"
            ],
            "classes": ["collapse"]
        }),
        (_("Site Header"), {
            "fields": [
                ("bg_tophead"),
                ("txt_tophead"),
                ("hov_tophead")
            ]
        }),
        (_("Advertising Top Banner"), {
            "fields": [
                ("bg_topbar"),
                ("txt_topbar"),
                ("hov_topbar")
            ],
            "classes": ["collapse"]
        }),
        (_("Main Navigation"), {
            "fields": [
                ("bg_topnav"),
                ("txt_topnav"),
                ("hov_topnav")
            ],
            "classes": ["collapse"]
        }),
        (_("Main Navigation Sub-menu"), {
            "fields": [
                ("bg_topsubnav"),
                ("txt_topsubnav"),
                ("hov_topsubnav")
            ],
            "classes": ["collapse"]
        }),
        (_("Site Footer"), {
            "fields": [
                "bg_footer",
                "txt_footer",
                "ttl_footer",
                "lnk_footer",
                "lnk_hov_footer"
            ]
        }),
        (_("Copyright Banner"), {
            "fields": [
                "bg_footcopy",
                "sep_footcopy",
                "txt_footcopy",
                "lnk_footcopy",
                "lnk_hov_footcopy"
            ],
            "classes": ["collapse"]
        }),
        (_("Default Page Header"), {
            "fields": [
                "bg_pagehead",
                "txt_pagehead",
                "lnk_pagehead",
                "lnk_hov_pagehead"
            ]
        })
    ]
