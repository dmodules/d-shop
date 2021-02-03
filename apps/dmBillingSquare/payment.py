import re
import uuid

from settings import CLIENT_TITLE, SHOP_VENDOR_EMAIL
from settings import SQUARE_APIKEY, SQUARE_TOKEN, SQUARE_LOCATION_ID, SQUARE_ENVIRONMENT

from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site

from rest_framework.exceptions import ValidationError

from square.client import Client

from shop.payment.providers import PaymentProvider
from shop.models.order import OrderModel

try:
    from apps.dmRabais.models import dmCustomerPromoCode
except ImportError:
    dmCustomerPromoCode = None

square_apikey = SQUARE_APIKEY
square_token = SQUARE_TOKEN
square_location = SQUARE_LOCATION_ID
square_environment = SQUARE_ENVIRONMENT
square_merchantemail = SHOP_VENDOR_EMAIL

#######################################################################
# ===---   SquarePayment                                       ---=== #
#######################################################################

class SquarePayment(PaymentProvider):
    """
    Provides a payment service for Square.
    """
    namespace = "square-payment"

    def get_payment_request(self, cart, request):  # noqa: C901
        print("Do Square Payment Request")
        #
        SITE_LINK = str(Site.objects.first().domain)
        if not SITE_LINK.startswith("http"):
            SITE_LINK = "https://" + SITE_LINK
        #
        try:
            order = OrderModel.objects.create_from_cart(cart, request)
            order_number = order.get_number()
            client = Client(access_token=square_token, environment=square_environment)
            checkout_api = client.checkout
            # =========---
            order.populate_from_cart(cart, request)
            order.save()
            # =========---
            body = {}
            body['idempotency_key'] = str(uuid.uuid1())
            body['redirect_url'] = SITE_LINK+'/billing-square/payment/'
            body['order'] = {}
            body['order']['order'] = {}
            body['order']['order']['location_id'] = square_location
            body['order']['order']['reference_id'] = order_number
            body['order']['order']['source'] = {}
            body['order']['order']['source']['name'] = CLIENT_TITLE
            body['order']['order']['customer_id'] = 'customer_id'
            body['order']['order']['line_items'] = []
            # ===---
            for n, item in enumerate(order.items.values()):
                body['order']['order']['line_items'].append({})
                body['order']['order']['line_items'][n]['uid'] = str(uuid.uuid1())
                body['order']['order']['line_items'][n]['name'] = str(item['product_name'])
                body['order']['order']['line_items'][n]['quantity'] = str(item['quantity'])
                body['order']['order']['line_items'][n]['base_price_money'] = {}
                body['order']['order']['line_items'][n]['base_price_money']['amount'] = int(item['_unit_price'] * 100)
                body['order']['order']['line_items'][n]['base_price_money']['currency'] = 'CAD'
                body['order']['order']['line_items'][n]['applied_taxes'] = []
                body['order']['order']['line_items'][n]['applied_taxes'].append({})
                body['order']['order']['line_items'][n]['applied_taxes'][0]['uid'] = str(uuid.uuid1())
                body['order']['order']['line_items'][n]['applied_taxes'][0]['tax_uid'] = 'total-taxes'
                body['order']['order']['line_items'][n]['applied_discounts'] = []
                body['order']['order']['line_items'][n]['applied_discounts'].append({})
                body['order']['order']['line_items'][n]['applied_discounts'][0]['uid'] = str(uuid.uuid1())
                body['order']['order']['line_items'][n]['applied_discounts'][0]['discount_uid'] = 'total-discounts'
            # ===---
            body['order']['order']['taxes'] = []
            for key, item in order.extra['rows']:
                if key == 'canadiantaxes':
                    body['order']['order']['taxes'].append({})
                    body['order']['order']['taxes'][0]['uid'] = 'total-taxes'
                    body['order']['order']['taxes'][0]['name'] = str(_('Taxes'))
                    body['order']['order']['taxes'][0]['percentage'] = str(item['label'].split('%')[0])
                    body['order']['order']['taxes'][0]['scope'] = 'LINE_ITEM'
                if key == 'discounts':
                    body['order']['order']['discounts'] = []
                    body['order']['order']['discounts'].append({})
                    body['order']['order']['discounts'][0]['uid'] = 'total-discounts'
                    body['order']['order']['discounts'][0]['name'] = str(_('Discounts'))
                    body['order']['order']['discounts'][0]['amount_money'] = {}
                    body['order']['order']['discounts'][0]['amount_money']['amount'] = int(float(
                        re.sub('[^0-9,.]', '', item['amount'].replace(',', '.'))
                    ) * 100)
                    body['order']['order']['discounts'][0]['amount_money']['currency'] = 'CAD'
                    body['order']['order']['discounts'][0]['scope'] = 'LINE_ITEM'
                if key in [
                    "standard-shipping",
                    "express-shipping",
                    "standard-separator-shipping",
                    "express-separator-shipping"
                ]:
                    shipping = int(float(re.sub('[^0-9,.]', '', item['amount'].replace(',', '.'))) * 100)
                    shipping_data = {}
                    shipping_data['uid'] = str(uuid.uuid1())
                    shipping_data['name'] = str(item['label'])
                    shipping_data['quantity'] = '1'
                    shipping_data['base_price_money'] = {}
                    shipping_data['base_price_money']['amount'] = shipping
                    shipping_data['base_price_money']['currency'] = 'CAD'
                    body['order']['order']['line_items'].append(shipping_data)
            # ===---
            body['order']['location_id'] = str(uuid.uuid1())
            body['order']['idempotency_key'] = str(uuid.uuid1())
            body['merchant_support_email'] = square_merchantemail
            # =========---
            result = checkout_api.create_checkout(square_location, body)
            # ===---
            if result.is_success():
                res = result.body['checkout']['checkout_page_url']
                js_expression = 'window.location.href="{}";'.format(res)
                return js_expression
            elif result.is_error():
                print(result)
                raise ValidationError(_("An error occurred while creating your order."))
        except Exception as e:
            print(e)
            raise ValidationError(_("An error occurred while creating your order."))
