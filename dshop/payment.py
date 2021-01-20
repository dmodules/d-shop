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
        try:
            order = OrderModel.objects.create_from_cart(cart, request)
            referenceId = order.get_number()
            transactionId = str(uuid.uuid1())
            order.populate_from_cart(cart, request)
            order.save()
            redirect_url = "/test-payment/?referenceId=" + \
                str(referenceId) + "&transactionId=" + str(transactionId)
            js_expression = "window.location.href='{}';".format(redirect_url)
            return js_expression
        except Exception as e:
            print(e)
            raise ValidationError(
                _("An error occured while creating your order.")
            )
