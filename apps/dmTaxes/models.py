from django.utils.translation import ugettext_lazy as _
from django.db import models

try:
  from apps.dmBillingStripe.stripe_tax import create_tax
except:
  pass

#######################################################################
# Canada Taxes
#######################################################################

class CanadaTaxManagement(models.Model):
  state = models.CharField(
    _("Province"),
    choices=[2 * ('{}'.format(t),)
              for t in ['Alberta', 'British Columbia', 'Manitoba',
                        'New-Brunswick', 'Newfoundland and Labrador',
                        'Northwest Territories', 'Nova Scotia', 'Nunavut',
                        'Ontario', 'Prince Edward Island', 'Quebec',
                        'Saskatchewan', 'Yukon']],
    max_length=60,
    unique=True
  )
  hst = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
  gst = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
  pst = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
  qst = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
  stripe_hst = models.CharField(max_length=50, null=True, blank=True)
  stripe_gst = models.CharField(max_length=50, null=True, blank=True)
  stripe_pst = models.CharField(max_length=50, null=True, blank=True)
  stripe_qst = models.CharField(max_length=50, null=True, blank=True)

  class Meta:
    verbose_name = _("Taxe canadienne")
    verbose_name_plural = _("Taxes canadiennes")

  def __str__(self):
    return self.state

  def save(self, *args, **kwargs):
    if self._state.adding:
      hst, gst, pst, qst = create_tax(self)
      self.stripe_hst = hst
      self.stripe_gst = gst
      self.stripe_pst = pst
      self.stripe_qst = qst
    super(CanadaTaxManagement, self).save(*args, **kwargs)
