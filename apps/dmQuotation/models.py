from django.utils.translation import ugettext_lazy as _
from django.db import models
from shop.models.fields import JSONField
from shop.money.fields import MoneyField
from django.core.validators import MinValueValidator
from shop.models.customer import CustomerModel


class dmQuotation(models.Model):

    CHOICE_STATUS = [
        (1, _("CREATED")),
        (2, _("SUBMITTED")),
        (3, _("APPROVED")),
        (4, _("ORDERED")),
        (5, _("REJECTED"))
    ]

    customer = models.ForeignKey(
        CustomerModel,
        on_delete=models.CASCADE,
        related_name="customer",
        null=True, blank=True
    )
    cookie = models.CharField(
        verbose_name=_("Cookie ID"),
        max_length=100,
        null=True, blank=True
    )
    number = models.CharField(
        verbose_name=_("Quotation Number"),
        max_length=100,
    )
    status = models.PositiveSmallIntegerField(
        verbose_name=_("Quotation Status"),
        choices=CHOICE_STATUS,
        default=1,
    )
    created_at = models.DateTimeField(
        verbose_name=_("Quotation Created at"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Quotation Updated at"),
        auto_now=True
    )
    extra = JSONField(verbose_name=_("Extra fields"))
    stored_request = JSONField(blank=True, null=True)

    class Meta:
        verbose_name = _("Quotation")
        verbose_name_plural = _("Quotations")

    def __str__(self):
        return self.number


class dmQuotationItem(models.Model):

    CHOICE_TYPE = [
        (1, _("Default")),
        (2, _("Variable")),
    ]
    quotation = models.ForeignKey(
        dmQuotation,
        on_delete=models.CASCADE,
        related_name="quotation",
    )
    product_name = models.CharField(
        _("Product's Name"),
        max_length=255,
    )
    product_type = models.PositiveSmallIntegerField(
        verbose_name=_("Product Type"),
        choices=CHOICE_TYPE,
        default=1,
    )
    product_code = models.CharField(
        _("Product's Code"),
        max_length=255,
        null=True, blank=True
    )
    variant_code = models.CharField(
        _("Variant's Code"),
        max_length=255,
        null=True, blank=True
    )
    variant_attribute = models.CharField(
        _("Variant Attribute"),
        max_length=100,
        null=True, blank=True
    )
    unit_price = MoneyField(
        _("Unit Price"),
        decimal_places=3,
        null=True, blank=True
    )
    quantity = models.PositiveIntegerField(
        _("Quantity"),
        default=0,
        validators=[MinValueValidator(0)],
    )

    def __str__(self):
        return self.quotation.number + self.product_name
