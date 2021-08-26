from django.utils.translation import ugettext_lazy as _
from django.db import models

from datetime import datetime


class dmStockLog(models.Model):

    CHOICE_TYPE = [
        (1, _("Dshop to Square")),
        (2, _("Square to Dshop")),
    ]
    product_name = models.CharField(
        verbose_name=_("Product Name"),
        max_length=255,
    )
    product_square_code = models.CharField(
        verbose_name=_("Product Square Code"),
        max_length=255,
    )
    variant_square_code = models.CharField(
        verbose_name=_("Variant Square Code"),
        max_length=255,
    )
    old_quantity = models.IntegerField(
        _("Old Quantity"),
        default=0,
    )
    new_quantity = models.IntegerField(
        _("New Quantity"),
        default=0,
    )
    stock_update_date = models.DateTimeField(
        verbose_name=_("Stock Adjustment"),
        default=datetime.now
    )
    update_from = models.PositiveSmallIntegerField(
        verbose_name=_("Stock Updated From"),
        choices=CHOICE_TYPE,
        default=2
    )

    class Meta:
        verbose_name = _("Stock Log")
        verbose_name_plural = _("Stocks Log")

    def __str__(self):
        return self.product_name
