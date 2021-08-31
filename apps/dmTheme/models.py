from django.db import models
from django.utils.translation import ugettext_lazy as _

from colorfield.fields import ColorField


class dmTheme(models.Model):
    CHOIX_RAD_BUTTON = [
        ("2rem", _("Circle")),
        (".25rem", _("Rounded")),
        ("0", _("Square"))
    ]
    CHOIX_RAD_INPUT = [
        ("32px", _("Circle")),
        ("4px", _("Rounded")),
        ("0", _("Square"))
    ]
    CHOIX_RAD_CHECKBOX = [
        ("50%", _("Circle")),
        ("4px", _("Rounded")),
        ("0", _("Square"))
    ]
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        blank=False,
        null=False,
        help_text=_("A name used to recognize your custom themes.")
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
        help_text=_("Only the last created active theme will be used.")
    )
    bg_base = ColorField(
        verbose_name=_("Site Background's Colour"),
        default="#fbfbfb",
        blank=False,
        null=False,
        help_text=_("Applied to the site background.")
    )
    txt_base = ColorField(
        verbose_name=_("Site Text's Colour"),
        default="#202325",
        blank=False,
        null=False,
        help_text=_("Applied to the site default text.")
    )
    lnk_base = ColorField(
        verbose_name=_("Site Link's Colour"),
        default="#066bf9",
        blank=False,
        null=False,
        help_text=_("Applied to the site default link text.")
    )
    hov_base = ColorField(
        verbose_name=_("Site Hover's Colour"),
        default="#202325",
        blank=False,
        null=False,
        help_text=_("Applied to the site default link text on hover.")
    )
    # ===--- Button
    rad_button = models.CharField(
        verbose_name=_("Button's Shape"),
        max_length=10,
        choices=CHOIX_RAD_BUTTON,
        default=".25rem",
        blank=False,
        null=False,
        help_text=_("Applied to the site default buttons.")
    )
    txt_button = ColorField(
        verbose_name=_("Button Text's Colour"),
        default="#fbfbfb",
        blank=False,
        null=False,
        help_text=_("Applied to the site default buttons text.")
    )
    bor_button = ColorField(
        verbose_name=_("Button Border's Colour"),
        default="#066bf9",
        blank=False,
        null=False,
        help_text=_("Applied to the site default buttons border.")
    )
    bg_button = ColorField(
        verbose_name=_("Button Background's Colour"),
        default="#066bf9",
        blank=False,
        null=False,
        help_text=_("Applied to the site default buttons background.")
    )
    txt_hov_button = ColorField(
        verbose_name=_("Button Text's Hover Colour"),
        default="#fbfbfb",
        blank=False,
        null=False,
        help_text=_("Applied to the site default buttons text on hover.")
    )
    bor_hov_button = ColorField(
        verbose_name=_("Button Border's Colour"),
        default="#066bf9",
        blank=False,
        null=False,
        help_text=_("Applied to the site default buttons border on hover.")
    )
    bg_hov_button = ColorField(
        verbose_name=_("Button Background's Hover Colour"),
        blank=True,
        null=True,
        help_text=_("Applied to the site default buttons background on hover. \
            Leave blank to use transparent.")
    )
    # ===--- Input
    rad_input = models.CharField(
        verbose_name=_("Input's Shape"),
        max_length=5,
        choices=CHOIX_RAD_INPUT,
        default="4px",
        blank=False,
        null=False,
        help_text=_("Applied to the site default inputs (ex: \
            on the contact page).")
    )
    bg_input = ColorField(
        verbose_name=_("Input Background's Colour"),
        default="#fff",
        blank=False,
        null=False,
        help_text=_("Applied to the site default inputs (ex: \
            on the contact page).")
    )
    bor_input = ColorField(
        verbose_name=_("Input Border's Colour"),
        default="#ced4da",
        blank=False,
        null=False,
        help_text=_("Applied to the site default inputs (ex: \
            on the contact page).")
    )
    txt_input = ColorField(
        verbose_name=_("Input Text's Colour"),
        default="#202325",
        blank=False,
        null=False,
        help_text=_("Applied to the site default inputs (ex: \
            on the contact page).")
    )
    # ===--- Checkbox
    rad_checkbox = models.CharField(
        verbose_name=_("Checkbox's Shape"),
        max_length=5,
        choices=CHOIX_RAD_CHECKBOX,
        default="4px",
        blank=False,
        null=False,
        help_text=_("Applied to the site default checkboxes (ex: \
            on the products list page).")
    )
    bco_checkbox = ColorField(
        verbose_name=_("Checkbox's Colour"),
        default="#ced4da",
        blank=False,
        null=False,
        help_text=_("Applied to the site default checkboxes (ex: \
            on the products list page).")
    )
    act_checkbox = ColorField(
        verbose_name=_("Checked Checkbox's Colour"),
        default="#066bf9",
        blank=False,
        null=False,
        help_text=_("Applied to the site default checkboxes background when \
            checked (ex: on the products list page).")
    )
    act_chk_checkbox = ColorField(
        verbose_name=_("Checked Checkbox Check's Colour"),
        default="#fbfbfb",
        blank=False,
        null=False,
        help_text=_("Applied to the site default checkboxes check when \
            checked (ex: on the products list page).")
    )
    # ===--- Header
    bg_topbar = ColorField(
        verbose_name=_("Advertising Banner Background's Colour"),
        default="#eeeeee",
        blank=False,
        null=False,
        help_text=_("Applied to the advertising banner background.")
    )
    txt_topbar = ColorField(
        verbose_name=_("Advertising Banner Text's Colour"),
        default="#202325",
        blank=False,
        null=False,
        help_text=_("Applied to the advertising banner text.")
    )
    hov_topbar = ColorField(
        verbose_name=_("Advertising Banner Text's Hover Colour"),
        default="#066bf9",
        blank=False,
        null=False,
        help_text=_("Applied to the advertising banner text on hover.")
    )
    bg_tophead = ColorField(
        verbose_name=_("Header Banner Background's Colour"),
        default="#ffffff",
        blank=False,
        null=False,
        help_text=_("Applied to the site header banner background.")
    )
    txt_tophead = ColorField(
        verbose_name=_("Header Banner Text's Colour"),
        default="#202325",
        blank=False,
        null=False,
        help_text=_("Applied to the site header banner text.")
    )
    hov_tophead = ColorField(
        verbose_name=_("Header Banner Text's Hover Colour"),
        default="#066bf9",
        blank=False,
        null=False,
        help_text=_("Applied to the site header banner text on hover.")
    )
    # ===--- Main Menu
    bg_topnav = ColorField(
        verbose_name=_("Main Navigation Background's Colour"),
        default="#141617",
        blank=False,
        null=False,
        help_text=_("Applied to the main navigation background.")
    )
    txt_topnav = ColorField(
        verbose_name=_("Main Navigation Text's Colour"),
        default="#ffffff",
        blank=False,
        null=False,
        help_text=_("Applied to the main navigation text.")
    )
    hov_topnav = ColorField(
        verbose_name=_("Main Navigation Text's Hover Colour"),
        default="#066bf9",
        blank=False,
        null=False,
        help_text=_("Applied to the site main navigation text on hover.")
    )
    bg_topsubnav = ColorField(
        verbose_name=_("Main Navigation Sub-Menu Background's Colour"),
        default="#ffffff",
        blank=False,
        null=False,
        help_text=_("Applied to the main navigation sub-menu background.")
    )
    txt_topsubnav = ColorField(
        verbose_name=_("Main Navigation Sub-Menu Text's Colour"),
        default="#141617",
        blank=False,
        null=False,
        help_text=_("Applied to the main navigation sub-menu text.")
    )
    hov_topsubnav = ColorField(
        verbose_name=_("Main Navigation Sub-Menu Text's Hover Colour"),
        default="#066bf9",
        blank=False,
        null=False,
        help_text=_("Applied to the site main navigation sub-menu text \
            on hover.")
    )
    # ===--- Footer
    bg_footer = ColorField(
        verbose_name=_("Footer Background's Colour"),
        default="#202325",
        blank=False,
        null=False,
        help_text=_("Applied to the site footer background.")
    )
    txt_footer = ColorField(
        verbose_name=_("Footer Text's Colour"),
        default="#fbfbfb",
        blank=False,
        null=False,
        help_text=_("Applied to the site footer text.")
    )
    ttl_footer = ColorField(
        verbose_name=_("Footer Title's Colour"),
        default="#fbfbfb",
        blank=False,
        null=False,
        help_text=_("Applied to the site footer title.")
    )
    lnk_footer = ColorField(
        verbose_name=_("Footer Link's Colour"),
        default="#fbfbfb",
        blank=False,
        null=False,
        help_text=_("Applied to the site footer link.")
    )
    lnk_hov_footer = ColorField(
        verbose_name=_("Footer Link's Hover Colour"),
        default="#066bf9",
        blank=False,
        null=False,
        help_text=_("Applied to the site footer link on hover.")
    )
    bg_footcopy = ColorField(
        verbose_name=_("Copyright Background's Colour"),
        default="#202325",
        blank=False,
        null=False,
        help_text=_("Applied to the site copyright banner background.")
    )
    sep_footcopy = ColorField(
        verbose_name=_("Copyright Separator's Colour"),
        default="#37393b",
        blank=False,
        null=False,
        help_text=_("Applied to the site copyright banner separator.")
    )
    txt_footcopy = ColorField(
        verbose_name=_("Copyright Text's Colour"),
        default="#fbfbfb",
        blank=False,
        null=False,
        help_text=_("Applied to the site copyright banner text.")
    )
    lnk_footcopy = ColorField(
        verbose_name=_("Copyright Link's Colour"),
        default="#fbfbfb",
        blank=False,
        null=False,
        help_text=_("Applied to the site copyright banner link.")
    )
    lnk_hov_footcopy = ColorField(
        verbose_name=_("Copyright Link's Hover Colour"),
        default="#066bf9",
        blank=False,
        null=False,
        help_text=_("Applied to the site copyright banner link on hover.")
    )
    # ===--- Page Header
    bg_pagehead = ColorField(
        verbose_name=_("Page Header Background's Colour"),
        default="#f7f8fb",
        blank=False,
        null=False,
        help_text=_("Applied to the default page header background.")
    )
    txt_pagehead = ColorField(
        verbose_name=_("Page Header Text's Colour"),
        default="#202325",
        blank=False,
        null=False,
        help_text=_("Applied to the default page header text.")
    )
    lnk_pagehead = ColorField(
        verbose_name=_("Page Header Link's Colour"),
        default="#202325",
        blank=False,
        null=False,
        help_text=_("Applied to the default page header link.")
    )
    lnk_hov_pagehead = ColorField(
        verbose_name=_("Page Header Link's Hover Colour"),
        default="#066bf9",
        blank=False,
        null=False,
        help_text=_("Applied to the default page header link on hover.")
    )

    class Meta:
        verbose_name = _("Theme")
        verbose_name_plural = _("Themes")
        ordering = ["-pk"]

    def __str__(self):
        return self.name
