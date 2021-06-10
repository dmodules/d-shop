import stripe

from decimal import Decimal

from settings import STRIPE_SECRET_KEY, SHOP_DEFAULT_CURRENCY

from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site

from rest_framework.exceptions import ValidationError

from shop.payment.providers import PaymentProvider
from shop.models.order import OrderModel

from apps.dmTaxes.models import CanadaTaxManagement

try:
    from apps.dmRabais.models import dmCustomerPromoCode
except ImportError:
    dmCustomerPromoCode = None

stripe.api_key = STRIPE_SECRET_KEY

#######################################################################
# ===---   StripePayment                                       ---=== #
#######################################################################


class StripePayment(PaymentProvider):
    namespace = 'stripe-payment'

    def get_payment_request(self, cart, request): # noqa
        token = request.GET.get('token', '')
        SITE_LINK = str(Site.objects.first().domain)
        if not SITE_LINK.startswith("http"):
            SITE_LINK = "https://" + SITE_LINK
        try:
            order = OrderModel.objects.create_from_cart(cart, request)
            referenceId = order.get_number()
            # Collect Tax data
            province = cart.shipping_address.province
            tax_data = []
            tax = CanadaTaxManagement.objects.filter(state=province)
            if tax:
                tax_data = []
                if tax[0].hst != Decimal('0'):
                    tax_data.append(tax[0].stripe_hst)
                if tax[0].gst != Decimal('0'):
                    tax_data.append(tax[0].stripe_gst)
                if tax[0].pst != Decimal('0'):
                    tax_data.append(tax[0].stripe_pst)
                if tax[0].qst != Decimal('0'):
                    tax_data.append(tax[0].stripe_qst)
            order.populate_from_cart(cart, request)
            order.save()
            # Collect Shipping cost
            shipping_cost = 0
            mod = order.extra.get('shipping_modifier')
            try:
                if mod:
                    for d in order.extra['rows']:
                        if d[0] == mod:
                            shipping_cost = order.extra['rows'][
                                order.extra['rows'].index(d)
                            ][1]['charge']
            except Exception as e:
                print("Error on Stripe Payment Shipping Cost : " + str(e))
                shipping_cost = order.extra['rows'][order.extra['rows'].index(
                    d)][1]['amount']
                if "," in shipping_cost:
                    shipping_cost_1 = shipping_cost.split(' ')[1].split(',')[0]
                    shipping_cost_2 = shipping_cost.split(' ')[1].split(',')[1]
                if "." in shipping_cost:
                    shipping_cost_1 = shipping_cost.split(' ')[1].split('.')[0]
                    shipping_cost_2 = shipping_cost.split(' ')[1].split('.')[1]

                s_c_1 = int(shipping_cost_1)
                s_c_2 = int(shipping_cost_2)
                shipping_cost = s_c_1 * 100 + s_c_2
            # site = SITE_LINK
            # success_url = site + \
            #     "/billing-stripe/payment/?referenceId="+str(referenceId)
            # cancel_url = site + \
            #     "/billing-stripe/cancel/?referenceId="+str(referenceId)
            line_items = []
            # Create product line data
            line_data = {
                "name": str(_("Order") + " #" + str(referenceId)),
                "quantity": "1",
                "currency": str(SHOP_DEFAULT_CURRENCY),
                "amount": str(int(order.subtotal * 100))
            }
            line_items.append(line_data)
            # Check if shipping is taxed
            shipping_taxed = False
            for d in order.extra['rows']:
                if d[0] in ["shipping-is-taxed"]:
                    shipping_taxed = True
            # Create shipping cost line data before taxe
            # if shipping is taxed
            if shipping_taxed:
                if shipping_cost != 0:
                    line_data = {
                        "name": _("Shipping"),
                        "quantity": 1,
                        "currency": str(SHOP_DEFAULT_CURRENCY),
                        "amount": shipping_cost
                    }
                    line_items.append(line_data)
            # Create Tax line data
            for d in order.extra['rows']:
                if d[0] in ["canadiantaxes"]:
                    line_data = {
                        "name": _("Taxes"),
                        "quantity": 1,
                        "currency": str(SHOP_DEFAULT_CURRENCY),
                        "amount": int(
                            float(
                                ".".join(
                                    d[1]['amount'].split(' ')[1].split(',')
                                )
                            ) * 100
                        )
                    }
                    line_items.append(line_data)
            # Create shipping cost line data after taxe
            # if shipping is not taxed
            if not shipping_taxed:
                if shipping_cost != 0:
                    line_data = {
                        "name": _("Shipping"),
                        "quantity": 1,
                        "currency": str(SHOP_DEFAULT_CURRENCY),
                        "amount": shipping_cost
                    }
                    line_items.append(line_data)

            # ===---
            total_amount = 0
            for data in line_items:
                total_amount += int(data['amount'])
            error = {}
            try:
                charge = stripe.Charge.create(
                    amount=total_amount,
                    currency='cad',
                    description=str(_("Order") + " #" + str(referenceId)),
                    source=token,
                )
                status = charge.status
            except Exception as e:
                status = ''
                error['code'] = e.error.code
                error['message'] = e.error.message

            if status == "succeeded":
                redirect_url = '/billing-stripe/payment/?referenceId=' + \
                    str(referenceId)+'&charge='+str(charge.id)
            else:
                redirect_url = '/billing-stripe/cancel/?referenceId=' + \
                    str(referenceId)+'&error_code='+str(error['code']) + \
                    '&error_message='+str(error['message'])
            js_expression = 'window.location.href="{}";'.format(redirect_url)
            return js_expression
        except Exception as e:
            print(e)
            raise ValidationError(
                _("An error occurred while creating your order.")
            )
