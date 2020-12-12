from django.utils.translation import ugettext_lazy as _
from django.db import models

#######################################################################
# Canada Taxes
#######################################################################

class ShippingManagement(models.Model):
  CHOICE_IDENTIFIER = [
    ('free-shipping', _('Envoi postal (gratuit)')),
    ('standard-shipping', _('Envoi postal (standard)')),
    ('express-shipping', _('Envoi postal (express)'))
  ]

  name = models.CharField(verbose_name=_("Nom de la méthode d'expédition"), max_length=255, blank=False, null=False)
  identifier = models.CharField(verbose_name=_("Identifiant"), max_length=100, choices=CHOICE_IDENTIFIER, default='free-shipping', unique=True, blank=False, null=False)
  price = models.DecimalField(_("Prix"), max_digits=30, decimal_places=3, help_text=_("Un prix fixe ajouté au prix total du panier."))

  class Meta:
    verbose_name = _("Méthode d'expédition")
    verbose_name_plural = _("Méthodes d'expédition")

  def get_price(self):
    return str(self.price)
  get_price.short_description = _("Prix")
