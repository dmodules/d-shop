from django.utils.translation import ugettext_lazy as _
from django.db import models

#######################################################################
# Shipping Methods
#######################################################################


class ShippingManagement(models.Model):
    """A model to handle Standard Shipping Methods"""

    CHOICE_IDENTIFIER = [
        (
            "pickup-in-store",
            _("Pick Up in Store")
        ),
        (
            "free-shipping",
            _("Postal shipping (free)")
        ),
        (
            "standard-shipping",
            _("Postal shipping (standard)")
        ),
        (
            "express-shipping",
            _("Postal shipping (express)")
        ),
        (
            "standard-separator-shipping",
            _("Postal shipping with separator (standard)")
        ),
        (
            "express-separator-shipping",
            ("Postal shipping with separator (express)")
        ),
    ]

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        blank=False,
        null=False,
        help_text=_("Maximum 255 characters.")
    )
    identifier = models.CharField(
        verbose_name=_("Identifier"),
        max_length=100,
        choices=CHOICE_IDENTIFIER,
        default="free-shipping",
        unique=True,
        blank=False,
        null=False
    )
    price = models.DecimalField(
        _("Price"),
        max_digits=30,
        decimal_places=3,
        help_text=_("An amount to be added to the cart price.")
    )
    use_separator = models.BooleanField(
        verbose_name=_("Use an amount to separate two price?"),
        default=True
    )
    separator = models.DecimalField(
        verbose_name=_("Amount to reach to get the discount"),
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        help_text=_("The amount of the cart price to separate the shipping price before and after it.")
    )
    price_after = models.DecimalField(
        verbose_name=_("Shipping price when the amount has been reached"),
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        help_text=_("The price to replace the original shipping price if the separator's amount has been reached.")
    )

    class Meta:
        verbose_name = _("Shipping Method")
        verbose_name_plural = _("Shipping Methods")
        ordering = ["name", "-pk"]

    def get_price(self):
        return str(self.price)

    get_price.short_description = _("Price")
