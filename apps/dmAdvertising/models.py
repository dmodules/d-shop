from django.utils.translation import ugettext_lazy as _
from django.db import models

from datetime import datetime

#######################################################################
# Alerte Publicitaire
#######################################################################

class dmAdvertisingTopBanner(models.Model):
  """Model for Advertising Alert on a banner on top of the website"""
  text = models.CharField(
    verbose_name=_("Texte"),
    max_length=75,
    help_text=_("Maximum de 75 caractères.")
  )
  link = models.CharField(
    verbose_name=_("Lien URL"),
    max_length=1000,
    blank=True,
    null=True,
    help_text=_("Exemple: https://www.test.com. Laissez vide pour ne pas utiliser de lien.")
  )
  open_blank = models.BooleanField(
    verbose_name=_("Ouvrir le lien dans un nouvel onglet ?"),
    default=False
  )
  is_active = models.BooleanField(
    verbose_name=_("Actif"),
    default=True
  )
  valid_from = models.DateTimeField(
    verbose_name=_("Date de début"),
    default=datetime.now
  )
  valid_until = models.DateTimeField(
    verbose_name=_("Date de fin"),
    blank=True,
    null=True
  )

  class Meta:
    verbose_name = _("Banderole d'entête publicitaire")
    verbose_name_plural = _("Banderoles d'entête publicitaires")

  def __str__(self):
    return self.text
