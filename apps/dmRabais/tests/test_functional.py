
import pytz
from django.test import TestCase
from datetime import datetime, timedelta

from .utils import \
    create_discount
from dshop.models import Product
from dshop.tests.utils import \
    category, \
    product


class CategoryDiscountTestProduct(TestCase):

    def setUp(self):
        self.cat = category()
        product(None, self.cat)

    def test_discounted_price(self):
        prod = Product.objects.all().first()

        prod.discounted_price = 50
        prod.start_date = pytz.utc.localize(datetime.today() - timedelta(days=2))
        prod.end_date = pytz.utc.localize(datetime.today() + timedelta(days=2))
        prod.save()

        prod = Product.objects.all().first()
        new_price = prod.get_price()
        self.assertEqual(prod.discounted_price, new_price)

    def test_discounted_price_expire(self):
        prod = Product.objects.all().first()

        prod.discounted_price = 50
        prod.start_date = pytz.utc.localize(datetime.today() - timedelta(days=2))
        prod.end_date = pytz.utc.localize(datetime.today() - timedelta(days=1))
        prod.save()

        prod = Product.objects.all().first()
        new_price = prod.get_price()
        self.assertNotEqual(prod.discounted_price, new_price)

    def test_category_discount(self):
        prod = Product.objects.all().first()
        old_price = prod.get_price()
        amount = 10
        # Create discount
        create_discount()
        # Get new Price
        new_price = prod.get_price()
        self.assertEqual(
            float(old_price.to_eng_string()),
            float(new_price.to_eng_string()) + amount
        )
