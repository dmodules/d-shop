import uuid

from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import ValidationError

from shop.payment.providers import PaymentProvider
from shop.models.order import OrderModel

#######################################################################
# ===---   TestPayment                                         ---=== #
#######################################################################


class TestPayment(PaymentProvider):
    namespace = "test-payment"

    def get_payment_request(self, cart, request):
        print("do Test payment request")

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
            redirect_url = "/test-payment/?referenceId=" + \
                str(referenceId) + "&transactionId=" + str(transactionId)
            js_expression = "window.location.href='{}';".format(redirect_url)
            return js_expression
        except Exception as e:
            print(e)
            raise ValidationError(
                _("An error occured while creating your order.")
            )
