import stripe

from decimal import Decimal

from settings import STRIPE_SECRET_KEY

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
        print('Do Stripe Payment Request')
        #
        SITE_LINK = str(Site.objects.first().domain)
        if not SITE_LINK.startswith("http"):
            SITE_LINK = "https://" + SITE_LINK
        #
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
                                order.extra['rows'].index(d)][1]['charge']
            except Exception as e:
                print(e)
                shipping_cost = order.extra['rows'][order.extra['rows'].index(
                    d)][1]['amount']
                shipping_cost_1 = shipping_cost.split(' ')[1].split(',')[0]
                shipping_cost_2 = shipping_cost.split(' ')[1].split(',')[1]
                shipping_cost = int(shipping_cost_1) * 100 + int(shipping_cost_2)
            site = SITE_LINK
            success_url = site + \
                "/billing-stripe/payment/?referenceId="+str(referenceId)
            cancel_url = site + \
                "/billing-stripe/cancel/?referenceId="+str(referenceId)
            line_items = []
            # Create product line data
            for item in order.items.values():
                line_data = {
                    "name": str(item['product_name']),
                    "quantity": str(item['quantity']),
                    "currency": "cad",
                    "amount": str(int(item['_unit_price'] * 100))
                }
                line_items.append(line_data)
            # Create shipping cost line data
            if shipping_cost != 0:
                line_data = {
                    "name": "Shipping Price",
                    "quantity": 1,
                    "currency": "cad",
                    "amount": shipping_cost
                }
                line_items.append(line_data)
            # Create Tax line data
            for d in order.extra['rows']:
                if d[0] in ["data1", "data2", "data3", "data4"]:
                    line_data = {
                        "name": d[1]['label'],
                        "quantity": 1,
                        "currency": "cad",
                        "amount":
                        int(
                            float(".".join(d[1]['amount'].split(' ')[1].split(','))) * 100
                        )
                    }
                    line_items.append(line_data)
            # ===---
            try:
                if dmCustomerPromoCode is not None:
                    for extra in order.extra["rows"]:
                        if "applied-promocodes" in extra:
                            promo = extra[1]["content_extra"].split(", ")
                            for pm in promo:
                                cpc = dmCustomerPromoCode.objects.filter(
                                    customer=request.user.customer,
                                    promocode__code=pm
                                )
                                for ccpc in cpc:
                                    ccpc.is_expired = True
                                    ccpc.save()
            except Exception as e:
                print(e)
            # ===---
            session = stripe.checkout.Session.create(
                success_url=success_url,
                cancel_url=cancel_url,
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
            )
            redirect_url = '/billing-stripe/checkout/?referenceId=' + \
                str(referenceId)+'&session='+str(session['id'])
            js_expression = 'window.location.href="{}";'.format(redirect_url)
            return js_expression
        except Exception as e:
            print(e)
            raise ValidationError(_("An error occurred while creating your order."))
