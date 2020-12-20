from django.utils.translation import ugettext_lazy as _
from decimal import Decimal

from shop.money import Money
from shop.conf import app_settings
from shop.serializers.cart import ExtraCartRow
from shop.modifiers.base import BaseCartModifier

from dshop.models import ShippingAddress

from .models import CanadaTaxManagement

#######################################################################
# ===---   Taxes: Canada                                       ---=== #
#######################################################################


class CanadaTaxModifier(BaseCartModifier):
    identifier = 'canadiantaxes'
    taxes = 1 - 1 / (1 + app_settings.VALUE_ADDED_TAX / 100)

    def add_extra_cart_row(self, cart, request):
        amount = cart.subtotal * self.taxes
        instance = {
            'label': _("{}% VAT incl.").format(app_settings.VALUE_ADDED_TAX),
            'amount': amount,
        }
        try:
            shippingaddress = ShippingAddress.objects.filter(
                customer=request.customer).first()
            if shippingaddress:
                if shippingaddress.country == 'CA':
                    state = shippingaddress.province
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
                    tax = CanadaTaxManagement.objects.get(state=state)
                    hst = tax.hst if tax.hst else Decimal('0')
                    gst = tax.gst if tax.gst else Decimal('0')
                    pst = tax.pst if tax.pst else Decimal('0')
                    qst = tax.qst if tax.qst else Decimal('0')
                    tax = (hst + gst + pst + qst)
                    amount = cart.subtotal * tax / 100
                    instance = {
                        'label': _("{}% TOTAL incl.").format(tax),
                        'amount': amount,
                    }
        except:
            pass
        try:
            if hst != Decimal('0'):
                data1 = {
                    'label': _("{}% HST incl.").format(hst),
                    'amount': cart.subtotal * hst / 100,
                }
                cart.extra_rows['data1'] = ExtraCartRow(data1)
            if gst != Decimal('0'):
                data2 = {
                    'label': _("{}% GST incl.").format(gst),
                    'amount': cart.subtotal * gst / 100,
                }
                cart.extra_rows['data2'] = ExtraCartRow(data2)
            if pst != Decimal('0'):
                data3 = {
                    'label': _("{}% PST incl.").format(pst),
                    'amount': cart.subtotal * pst / 100,
                }
                cart.extra_rows['data3'] = ExtraCartRow(data3)
            if qst != Decimal('0'):
                data4 = {
                    'label': _("{}% QST incl.").format(qst),
                    'amount': cart.subtotal * qst / 100,
                }
                cart.extra_rows['data4'] = ExtraCartRow(data4)
        except:
            pass
        cart.extra_rows[self.identifier] = ExtraCartRow(instance)
        cart.total += amount
