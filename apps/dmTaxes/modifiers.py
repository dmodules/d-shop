import re
from decimal import Decimal

from django.utils.translation import ugettext_lazy as _

from shop.money import Money
from shop.conf import app_settings
from shop.serializers.cart import ExtraCartRow
from shop.modifiers.base import BaseCartModifier

from dshop.models import ShippingAddress
from dshop.serializers import ExtraCartRowContent

from apps.dmShipping.models import ShippingManagement

from .models import CanadaTaxManagement

#######################################################################
# ===---   Taxes: Canada                                       ---=== #
#######################################################################


class CanadaTaxModifier(BaseCartModifier):
    identifier = "canadiantaxes"
    taxes = 1 - 1 / (1 + app_settings.VALUE_ADDED_TAX / 100)

    def add_extra_cart_row(self, cart, request):  # noqa: C901
        # ===---
        if "shipping_modifier" in cart.extra:
            try:
                shipping_method = ShippingManagement.objects.filter(
                    identifier=cart.extra["shipping_modifier"]
                ).first()
                taxed_shipping = (
                    True if shipping_method.taxed_shipping else False
                )
            except Exception:
                taxed_shipping = False
        else:
            taxed_shipping = False
        # ===---
        if taxed_shipping:
            shiptotal = float(
                re.sub(
                    r"[^.\-\d]",
                    "",
                    cart.extra_rows[
                        cart.extra["shipping_modifier"]
                    ].data["amount"]
                )
            ) / 100
            shiptotal = Money(shiptotal)
            subtotal = cart.subtotal + shiptotal
            cart.extra_rows["shipping-is-taxed"] = ExtraCartRowContent({
                "label": _("Shipping is Taxed"),
                "content": _("Yes"),
                "content_extra": shiptotal
            })
        else:
            subtotal = cart.subtotal
        # ===---
        amount = subtotal * self.taxes
        instance = {
            "label": _("{}% VAT incl.").format(app_settings.VALUE_ADDED_TAX),
            "amount": amount,
        }
        # ===---
        try:
            shippingaddress = ShippingAddress.objects.filter(
                customer=request.customer
            ).first()
            if shippingaddress.country == 'CA':
                state = shippingaddress.province
                state = state_fr_to_en(state)
                tax = CanadaTaxManagement.objects.get(state=state)
                hst = tax.hst if tax.hst else Decimal('0')
                gst = tax.gst if tax.gst else Decimal('0')
                pst = tax.pst if tax.pst else Decimal('0')
                qst = tax.qst if tax.qst else Decimal('0')
                tax = (hst + gst + pst + qst)
                amount = subtotal * tax / 100
                instance = {
                    'label': _("{}% TOTAL incl.").format(tax),
                    'amount': amount,
                }
        except Exception:
            pass
        try:
            if hst != Decimal('0'):
                data1 = {
                    'label': _("{}% HST incl.").format(hst),
                    'amount': subtotal * hst / 100,
                }
                cart.extra_rows['data1'] = ExtraCartRow(data1)
            if gst != Decimal('0'):
                data2 = {
                    'label': _("{}% GST incl.").format(gst),
                    'amount': subtotal * gst / 100,
                }
                cart.extra_rows['data2'] = ExtraCartRow(data2)
            if pst != Decimal('0'):
                data3 = {
                    'label': _("{}% PST incl.").format(pst),
                    'amount': subtotal * pst / 100,
                }
                cart.extra_rows['data3'] = ExtraCartRow(data3)
            if qst != Decimal('0'):
                data4 = {
                    'label': _("{}% QST incl.").format(qst),
                    'amount': subtotal * qst / 100,
                }
                cart.extra_rows['data4'] = ExtraCartRow(data4)
        except Exception:
            pass
        cart.extra_rows[self.identifier] = ExtraCartRow(instance)
        cart.total += Money(round(Decimal(amount), 2))


def state_fr_to_en(state):
    if state == "Colombie-Britannique":
        state = "British Columbia"
    elif state == "Nouveau-Brunswick":
        state = "New-Brunswick"
    elif state == "Terre-Neuve et Labrador":
        state = "Newfoundland and Labrador"
    elif state == "Territoires du Nord-Ouest":
        state = "Northwest Territories"
    elif state == "Nouvelle-Écosse":
        state = "Nova Scotia"
    elif state == "Île-du-Prince-Édouard":
        state = "Prince Edward Island"
    elif state == "Québec":
        state = "Quebec"
    return state
