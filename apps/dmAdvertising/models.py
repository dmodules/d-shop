from django.utils.translation import ugettext_lazy as _
from django.db import models

from datetime import datetime

#######################################################################
# Alerte Publicitaire
#######################################################################


class dmAdvertisingTopBanner(models.Model):
    """Model for Advertising Alert on a banner on top of the website"""
    text = models.CharField(
        verbose_name=_("Text"),
        max_length=75,
        help_text=_("Maximum 75 characters.")
    )
    link = models.CharField(
        verbose_name=_("URL"),
        max_length=1000,
        blank=True,
        null=True,
        help_text=_("Example: https://www.test.com. Leave blank to not use link.")
    )
    open_blank = models.BooleanField(
        verbose_name=_("Open on a new tab?"),
        default=False
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True
    )
    valid_from = models.DateTimeField(
        verbose_name=_("Start at"),
        default=datetime.now
    )
    valid_until = models.DateTimeField(
        verbose_name=_("End at"),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("Advertising Top Banner")
        verbose_name_plural = _("Advertising Top Banners")

    def __str__(self):
        return self.text
