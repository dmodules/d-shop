
from django.utils.translation import ugettext_lazy as _
from django.db import models
from filer.fields import image

class dmPortfolio(models.Model):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=250,
        help_text=_("Maximum 250 characters.")
    )
    description = models.TextField(
        verbose_name=_("Description")
    )
    image = image.FilerImageField(
        verbose_name=_("Image"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    active = models.BooleanField(
        default=True,
        verbose_name=_("Active")
    )

    class Meta:
        verbose_name = _("Portfolio's Item")
        verbose_name_plural = _("Portfolio's Items")

    def __str__(self):
        return self.title
