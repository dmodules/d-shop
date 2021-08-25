from django.utils.translation import ugettext_lazy as _
from django.db import models
from cities_light.models import Country, City, Region
from parler.models import TranslatableModel, TranslatedField
from parler.models import TranslatedFieldsModel

#######################################################################
# Shipping Methods
#######################################################################


class ShippingManagement(TranslatableModel):
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

    name = TranslatedField()
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
    taxed_shipping = models.BooleanField(
        verbose_name=_("Tax shipping?"),
        default=False,
        help_text=_("Leave unchecked if you don't want to tax shipping.")
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
        help_text=_("The amount of the cart price to separate the shipping price before and after it.") # noqa
    )
    price_after = models.DecimalField(
        verbose_name=_("Shipping price when the amount has been reached"),
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        help_text=_("The price to replace the original shipping price if the separator's amount has been reached.") # noqa
    )

    class Meta:
        verbose_name = _("Shipping Method")
        verbose_name_plural = _("Shipping Methods")
        ordering = ["-pk"]

    def get_price(self):
        return str(self.price)

    get_price.short_description = _("Price")


class ShippingManagementTranslation(TranslatedFieldsModel):
    """
    A model to handle translations of Attribute
    """

    master = models.ForeignKey(
        ShippingManagement,
        on_delete=models.CASCADE,
        related_name="translations",
        null=True
    )
    name = models.CharField(
        verbose_name=_("Translated Attribute Name"),
        max_length=255,
    )

    class Meta:
        unique_together = [("language_code", "master")]


class ShippingCountry(models.Model):

    name = models.CharField(
        verbose_name=_("Country Name"),
        max_length=50,
        blank=False,
        null=False,
        help_text=_("Maximum 50 characters.")
    )
    code = models.CharField(
        verbose_name=_("Country Code"),
        max_length=10,
        blank=False,
        null=False,
        unique=True,
        help_text=_("Maximum 2 characters.")
    )

    class Meta:
        verbose_name = _("Shipping Country")
        verbose_name_plural = _("Shipping Countries")
        ordering = ["code", "-pk"]

    def __str__(self):
        return str(self.name) + " : " + str(self.code)


class ShippingState(models.Model):

    country = models.ForeignKey(
        ShippingCountry,
        on_delete=models.CASCADE,
        related_name="country",
        verbose_name=_("Country"),
        blank=False,
        null=False
    )
    name = models.CharField(
        verbose_name=_("State Name"),
        max_length=100,
        blank=False,
        null=False,
        help_text=_("Maximum 50 characters.")
    )
    code = models.CharField(
        verbose_name=_("State Code"),
        max_length=10,
        blank=False,
        null=False,
        help_text=_("Maximum 2 characters.")
    )

    class Meta:
        verbose_name = _("Shipping State")
        verbose_name_plural = _("Shipping States")
        ordering = ["country", "code"]

    def __str__(self):
        return str(self.country.name) + " : " + str(self.name) + " : " + str(self.code) # noqa


class ShippingCity(models.Model):

    state = models.ForeignKey(
        ShippingState,
        on_delete=models.CASCADE,
        related_name="state",
        verbose_name=_("State"),
        blank=False,
        null=False
    )
    name = models.CharField(
        verbose_name=_("City Name"),
        max_length=50,
        blank=False,
        null=False,
        help_text=_("Maximum 50 characters.")
    )
    code = models.CharField(
        verbose_name=_("City Code"),
        max_length=10,
        blank=False,
        null=False,
        help_text=_("Maximum 2 characters.")
    )

    class Meta:
        verbose_name = _("Shipping City")
        verbose_name_plural = _("Shipping Cities")
        ordering = ["state", "code"]

    def __str__(self):
        return str(self.state.name) + " : " + str(self.name) + " : " + str(self.code) # noqa


class ShippingAllowed(models.Model):

    shipping = models.ForeignKey(
        ShippingManagement,
        on_delete=models.CASCADE,
        verbose_name=_("Shipping Management"),
        blank=False,
        null=False
    )
    countries = models.ManyToManyField(
        Country,
        verbose_name=_("Countries"),
        blank=True
    )
    states = models.ManyToManyField(
        Region,
        verbose_name=_("States"),
        blank=True
    )
    cities = models.ManyToManyField(
        City,
        verbose_name=_("Cities"),
        blank=True
    )
    price = models.DecimalField(
        _("Price"),
        max_digits=30,
        decimal_places=3,
        help_text=_("An amount to be added to the cart price.")
    )
