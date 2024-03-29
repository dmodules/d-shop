import random
import string

from django.utils.translation import ugettext_lazy as _
from django.db import models

from datetime import datetime

from shop.models.defaults.customer import Customer

#######################################################################
# Rabais
#######################################################################


class dmRabaisPerCategory(models.Model):
    """A model to handle promo on specific product's categories"""
    CHOICE_TYPE = [
        (1, _("Amount Discount")),
        (2, _("Percent Discount")),
    ]
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=100,
        help_text=_("Maximum 100 characters.")
    )
    amount = models.DecimalField(
        verbose_name=_("Amount"),
        max_digits=30,
        decimal_places=3,
        blank=True,
        null=True,
        help_text=_("An amount to substract to the original price, leave blank to use 'Percent'.") # noqa
    )
    percent = models.PositiveSmallIntegerField(
        verbose_name=_("Percent"),
        blank=True,
        null=True,
        help_text=_("A percent to substract to the original price, unused if there's an 'Amount'.") # noqa
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True
    )
    can_apply_on_discounted = models.BooleanField(
        verbose_name=_("Can Apply On Discounted Product?"),
        default=False
    )
    valid_from = models.DateTimeField(
        verbose_name=_("Start at"),
        default=datetime.now
    )
    valid_until = models.DateTimeField(
        verbose_name=_("End at"),
        blank=True,
        null=True
    )
    categories = models.ManyToManyField(
        "dshop.ProductCategory",
        related_name="rabaispercategory",
        verbose_name=_("Categories")
    )

    class Meta:
        verbose_name = _("Discount Per Category")
        verbose_name_plural = _("Discounts Per Category")

    def __str__(self):
        return self.name


#######################################################################
# Promo Code
#######################################################################


class dmPromoCode(models.Model):
    """A model to handle promo code with or without ending date"""
    CHOICE_TYPE = [
        (1, _("Amount Discount")),
        (2, _("Percent Discount")),
    ]
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=100,
        blank=False,
        null=False,
        help_text=_("Maximum 100 characters.")
    )
    code = models.CharField(
        verbose_name=_("Code"),
        max_length=120,
        blank=True,
        null=False,
        help_text=_("Leave blank to auto-generate a random code.")
    )
    amount = models.DecimalField(
        verbose_name=_("Amount"),
        max_digits=30,
        decimal_places=3,
        blank=True,
        null=True,
        help_text=_("An amount to substract to the original price, leave blank to use 'Percent'.") # noqa
    )
    percent = models.PositiveSmallIntegerField(
        verbose_name=_("Percent"),
        blank=True,
        null=True,
        help_text=_("A percent to substract to the original price, unused if there's an 'Amount'.") # noqa
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True
    )
    allow_multiple = models.BooleanField(
        verbose_name=_("Allow multiple uses?"),
        default=False,
        help_text=_("Allow customers to use this code multiple time?")
    )
    can_apply_on_discounted = models.BooleanField(
        verbose_name=_("Can Apply On Discounted Product?"),
        default=False
    )
    apply_on_cart = models.BooleanField(
        verbose_name=_("Apply on cart's total only"),
        default=False,
        help_text=_("Check to apply this promocode on the cart's total instead of individual product.") # noqa
    )
    valid_from = models.DateTimeField(
        verbose_name=_("Start at"),
        default=datetime.now
    )
    valid_until = models.DateTimeField(
        verbose_name=_("End at"),
        blank=True,
        null=True,
        help_text=_("Leave blank if you doesn't want this code to expire after a specific time.") # noqa
    )
    valid_uses = models.PositiveSmallIntegerField(
        verbose_name=_("Number of Customer"),
        default=0,
        blank=False,
        null=False,
        help_text=_("Leave to 0 if you doesn't want this code to expire after a specific number of customer's uses.") # noqa
    )
    customer = models.ManyToManyField(
        Customer,
        related_name="customerpromo",
        verbose_name=_("Customers"),
        limit_choices_to={"recognized": 2},
        blank=True,
        help_text=_("Only allow these customers to use this code. Leave blank to allow anyone.") # noqa
    )
    categories = models.ManyToManyField(
        "dshop.ProductCategory",
        related_name="promocode",
        verbose_name=_("Categories"),
        blank=True,
        help_text=_("Leave blank if you want to apply to all product.")
    )
    products = models.ManyToManyField(
        "dshop.Product",
        related_name="promocode",
        verbose_name=_("Products"),
        blank=True,
        help_text=_("Leave blank if you want to apply to all product.")
    )

    class Meta:
        verbose_name = _("Promo Code")
        verbose_name_plural = _("Promo Codes")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code or self.code is None:
            self.code = ''.join(
                random.choice(string.ascii_letters) for i in range(10)
            )
        super(dmPromoCode, self).save(*args, **kwargs)


class dmCustomerPromoCode(models.Model):
    """A model to handle customer's promocodes"""

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name=_("Customer"),
        blank=False,
        null=False
    )
    promocode = models.ForeignKey(
        dmPromoCode,
        on_delete=models.CASCADE,
        verbose_name=_("Promo Code"),
        blank=False,
        null=False
    )
    is_expired = models.BooleanField(
        verbose_name=_("Expired"),
        default=False
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True,
        blank=True,
        null=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"),
        auto_now=True,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("Customer's Promo Code")
        verbose_name_plural = _("Customer's Promo Codes")

    def __str__(self):
        return self.promocode.name
