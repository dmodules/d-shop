from django.utils.translation import ugettext_lazy as _
from django.db import models

from datetime import datetime

from boutique.models import ProductCategory

#######################################################################
# Rabais
#######################################################################

class dmRabaisPerCategory(models.Model):
  name = models.CharField(_('Nom'), max_length=100)
  amount = models.DecimalField(verbose_name=_("Montant fixe"), max_digits=30, decimal_places=3, blank=True, null=True, help_text=_("Un montant fixe à retirer du prix original, laisser vide pour privilégier le pourcentage."))
  percent = models.PositiveSmallIntegerField(verbose_name=_("Pourcentage"), blank=True, null=True, help_text=_("Un pourcentage à retirer du prix original, ne sera pas utilisé s'il y a un montant dans 'Montant fixe'."))
  is_active = models.BooleanField(_('Actif'), default=True)
  valid_from = models.DateTimeField(_('Date de début'), default=datetime.now)
  valid_until = models.DateTimeField(_('Date de fin'), blank=True, null=True)
  categories = models.ManyToManyField(ProductCategory, related_name="rabaispercategory", verbose_name=_("Categories"))

  class Meta:
    verbose_name = _("Rabais par catégorie")
    verbose_name_plural = _("Rabais par catégorie")

  def __str__(self):
    return self.name
