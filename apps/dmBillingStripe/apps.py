from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class dmBillingStripeConfig(AppConfig):
    name = "apps.dmBillingStripe"
    verbose_name = _("Facturation Stripe")
