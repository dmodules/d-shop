
from django.core.management.base import BaseCommand
from django.db import transaction
from shop.models.order import OrderModel
from shop.models.order import OrderPayment
import stripe

from dshop.models import ProductDefault
from settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY

class Command(BaseCommand):

    def handle(self, **options): # noqa

        orders = OrderModel.objects.all()
        for order in orders:

            if 'cancel' in order.extra:
                continue
            # Check for order payment and status
            order_payment = OrderPayment.objects.filter(order=order)
            if order_payment and order.status == 'payment_confirmed':
                # Order payment is done so check next order
                continue

            # Generate Revert quantity
            cart = order.customer.cart
            order.readd_to_cart(cart)
            try:
                with transaction.atomic():
                    for item in cart.items.all():
                        db_product = item.product
                        if type(db_product) == ProductDefault:
                            print('Default product: ' + str(db_product.product_name))
                            db_product.quantity += item.quantity
                            db_product.save()
                        else:
                            print('Variable product: ' + str(db_product.product_name))
                            p_code = item.product_code
                            pv = db_product.variants.get(product_code=p_code)
                            pv.quantity += item.quantity
                            pv.save()
                # Param to identify order is timed out
                order.extra['cancel'] = '1'
                order.save()
            except Exception as e:
                print("Error to update quantity: " + str(e))
                # !TODO

            # Deacivate payment link
            print('Deactivate payment link')
            if order.extra['payment_modifier'] == 'stripe-payment':
                try:
                    session_id = order.extra["session_id"]
                    session = stripe.checkout.Session.retrieve(session_id)
                    payment_intent_id = session.payment_intent
                    stripe.PaymentIntent.cancel(payment_intent_id)
                except Exception as e:
                    print("Errer in link deactivate: " + str(e))

            print('Send email')
