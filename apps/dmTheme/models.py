from django.utils.translation import ugettext_lazy as _
from django.db import models

class ThemeManagement(models.Model):

    theme = models.CharField(
        verbose_name=_("Theme"),
        max_length=50
    )
    css = models.TextField(
        verbose_name=_('CSS'),
        null=True,
        blank=True
    )
    active = models.BooleanField(
        verbose_name=('Active'),
        default=False
    )   

    class Meta:
        verbose_name = _("Theme Setting")
        verbose_name_plural = _("Theme Settings")

    def __str__(self):
        return self.theme

