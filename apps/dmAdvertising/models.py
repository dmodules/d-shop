from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import models

from parler.fields import TranslatedField
from parler.managers import TranslatableManager, TranslatableQuerySet
from parler.models import TranslatableModel, TranslatableModelMixin
from parler.models import TranslatedFieldsModel, TranslatedFields

from filer.fields.image import FilerImageField

#######################################################################
# Alerte Publicitaire
#######################################################################


class dmAdvertisingTopBanner(TranslatableModel):
    """Model for Advertising Alert on a banner on top of the website"""

    text = TranslatedField()
    link = TranslatedField()
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
        default=timezone.now
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
        try:
            if self.text:
                return self.text
            return str(self.pk)
        except Exception:
            return str(self.pk)


class dmAdvertisingTopBannerTranslation(TranslatedFieldsModel):
    """
    A model to handle translations of dmAdvertisingTopBanner
    """

    master = models.ForeignKey(
        dmAdvertisingTopBanner,
        on_delete=models.CASCADE,
        related_name="translations",
        null=True
    )
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

    class Meta:
        unique_together = [("language_code", "master")]


class dmAdvertisingPopup(models.Model):
    """Model for Advertising Alert on a popup"""
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=75,
        help_text=_("Maximum 75 characters.")
    )
    image_fr = FilerImageField(
        verbose_name=_("Image FR"),
        on_delete=models.CASCADE,
        related_name="advertisingpopup_image",
        help_text=_("Recommended size: 800x600.")
    )
    image_en = FilerImageField(
        verbose_name=_("Image EN"),
        on_delete=models.CASCADE,
        related_name="advertisingpopup_image_en",
        null=True, blank=True,
        help_text=_("Recommended size: 800x600.")
    )
    link = models.CharField(
        verbose_name=_("URL Link"),
        max_length=1000,
        null=True,
        blank=True,
        help_text=_("Optional.")
    )
    close_30days = models.BooleanField(
        verbose_name=_("Hide for 30 days"),
        default=True,
        help_text=_("Hide popup for 30 days on close, otherwise, show it everytime.")
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True
    )
    valid_from = models.DateTimeField(
        verbose_name=_("Start at"),
        default=timezone.now
    )
    valid_until = models.DateTimeField(
        verbose_name=_("End at"),
        blank=True,
        null=True
    )
    shown = models.PositiveSmallIntegerField(
        verbose_name=_("Shown"),
        default=0,
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = _("Advertising Popup")
        verbose_name_plural = _("Advertising Popups")
        ordering = ["is_active", "-id"]

    def __str__(self):
        if self.valid_until is not None and self.is_active:
            if timezone.now() > self.valid_until:
                self.is_active = False
                self.save()
        return self.title
