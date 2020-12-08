import uuid
from django.utils.translation import ugettext_lazy as _
from decimal import Decimal

from rest_framework.exceptions import ValidationError

from shop.payment.providers import PaymentProvider
from shop.models.order import OrderModel

#######################################################################
# ===---   TestPayment                                         ---=== #
#######################################################################

class TestPayment(PaymentProvider):
  namespace = 'test-payment'

  def get_payment_request(self, cart, request):
    print('do Test payment request')

    ###########################################
    # THIS IS AN EXAMPLE PAYMENT PROVIDER
    ###########################################

    ###########################################
    #
    # Don't forget to register it in modifiers.py
    #
    ###########################################

    ###########################################
    # ===--- DO PROVIDER REQUEST
    # Here, call provider, make payment request
    # Don't forget to create order
    # >>> order = OrderModel.objects.create_from_cart(cart, request)
    # If success, populate order with cart
      # >>> order.populate_from_cart(cart, request)
      # >>> order.save(with_notification=True)
      # Get order reference ID
      # >>> referenceId = order.get_number()
      # Get transaction ID from provider
      # (it'll be used after order)
      # And pass referenceId and transactionId to redirect URL
      # >>> redirect_url = '/test-payment/?referenceId='+str(referenceId)+'&transactionId='+str(transactionId)
      # Then, return js
      # >>> return 'window.location.href="{}";'.format(redirect_url)
      # After that, create an OrderPayment in a view
      # (check TestPaymentView in views.py)
    # If fail, raise a ValidationError
      # >>> raise ValidationError(_("Une erreur est survenue lors de la création de votre commande."))
    ############################################

    try:
      order = OrderModel.objects.create_from_cart(cart, request)
      referenceId = order.get_number()
      transactionId = str(uuid.uuid1())
      # ===---
      # === call to provider here
      # ===---
      # ===--- IF SUCCESS
      order.populate_from_cart(cart, request)
      order.save(with_notification=True)
      redirect_url = '/test-payment/?referenceId='+str(referenceId)+'&transactionId='+str(transactionId)
      js_expression = 'window.location.href="{}";'.format(redirect_url)
      return js_expression
    except:
      raise ValidationError(_("Une erreur est survenue lors de la création de votre commande."))

#######################################################################
# ===---   SquarePayment                                       ---=== #
#######################################################################

class SquarePayment(PaymentProvider):
    namespace = 'square-payment'

    def get_payment_request(self, cart, request):

        print('get payment request')
        '''
        try:
          shippingaddress = ShippingAddress.objects.get(customer=cart.customer)

          order = OrderModel.objects.create_from_cart(cart, request)
          order_number = order.get_number()

          client = Client(access_token=square_token, environment=square_environment)
          checkout_api = client.checkout

          current_site = Site.objects.get_current()

          # =========---
          body = {}
          body['idempotency_key'] = str(uuid.uuid1())
          body['redirect_url'] = current_site.domain+'/fr/square/'
          body['order'] = {}
          body['order']['order'] = {}
          body['order']['order']['location_id'] = square_location
          body['order']['order']['reference_id'] = order_number
          body['order']['order']['source'] = {}
          body['order']['order']['source']['name'] = 'À ta beauté'
          body['order']['order']['customer_id'] = 'customer_id'
          body['order']['order']['line_items'] = []
          # ===---
          shipping_n = cart.items.all().count()
          for n, item in enumerate(cart.items.all()):
            unit_price = int(float(item.product.unit_price) * 100)
            body['order']['order']['line_items'].append({})
            body['order']['order']['line_items'][n]['uid'] = str(uuid.uuid1())
            body['order']['order']['line_items'][n]['name'] = item.product.product_name
            body['order']['order']['line_items'][n]['quantity'] = str(item.quantity)
            body['order']['order']['line_items'][n]['base_price_money'] = {}
            body['order']['order']['line_items'][n]['base_price_money']['amount'] = unit_price
            body['order']['order']['line_items'][n]['base_price_money']['currency'] = 'CAD'
            body['order']['order']['line_items'][n]['applied_taxes'] = []
            body['order']['order']['line_items'][n]['applied_taxes'].append({})
            body['order']['order']['line_items'][n]['applied_taxes'][0]['uid'] = str(uuid.uuid1())
            body['order']['order']['line_items'][n]['applied_taxes'][0]['tax_uid'] = 'total-taxes'
          # ===---
          body['order']['order']['taxes'] = []
          for key, item in cart.extra_rows.items():
            if key == 'taxes':
              percent = item.data['label'].split('%')[0]
              body['order']['order']['taxes'].append({})
              body['order']['order']['taxes'][0]['uid'] = 'total-taxes'
              body['order']['order']['taxes'][0]['name'] = 'Taxes'
              body['order']['order']['taxes'][0]['percentage'] = percent
              body['order']['order']['taxes'][0]['scope'] = 'LINE_ITEM'
            if key == 'postal-shipping':
              shipping = int(float(re.sub('[^0-9,.]', '', item.data['amount'].replace(',','.'))) * 100)
              shipping_data = {}
              shipping_data['uid'] = str(uuid.uuid1())
              shipping_data['name'] = 'Envoi postal'
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

          if result.is_success():
            order.populate_from_cart(cart, request)
            order.save()
            res = result.body['checkout']['checkout_page_url']
            js_expression = 'window.location.href="{}";'.format(res)
            return js_expression
          elif result.is_error():
            # res = "Exception when calling checkout_api->create_checkout: {}".format(result.errors)
            # res = "Une erreur est survenue lors de la création de votre commande."
            # return res
            raise ValidationError("Une erreur est survenue lors de la création de votre commande.")
        except:
          raise ValidationError("Une erreur est survenue lors de la création de votre commande.")
        '''
