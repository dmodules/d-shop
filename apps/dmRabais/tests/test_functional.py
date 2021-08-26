
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
        prod.start_date = pytz.utc.localize(datetime.today() - timedelta(days=2)) # noqa
        prod.end_date = pytz.utc.localize(datetime.today() + timedelta(days=2))
        prod.save()

        prod = Product.objects.all().first()
        new_price = prod.get_price()
        self.assertEqual(prod.discounted_price, new_price)

    def test_discounted_price_expire(self):
        prod = Product.objects.all().first()

        prod.discounted_price = 50
        prod.start_date = pytz.utc.localize(datetime.today() - timedelta(days=2)) # noqa
        prod.end_date = pytz.utc.localize(datetime.today() - timedelta(days=1)) # noqa
        prod.save()

        prod = Product.objects.all().first()
        new_price = prod.get_price()
        self.assertNotEqual(prod.discounted_price, new_price)

    def test_category_discount(self):
        prod = Product.objects.all().first()
        old_price = prod.get_price()
        amount = float(10.00)
        # Create discount
        cat = create_discount()
        prod.categories.add(cat)
        # Get new Price
        new_price = prod.get_price()
        self.assertEqual(
            float(old_price.to_eng_string()),
            float(new_price.to_eng_string()) + amount
        )

    def test_category_discount_percent(self):
        data = {
            'name': 'Test Discount',
            'percent': 10,
            'is_active': True,
            'valid_from': pytz.utc.localize(datetime.today() - timedelta(days=2)), # noqa
            'valid_until': pytz.utc.localize(datetime.today() + timedelta(days=3)), # noqa
        }
        prod = Product.objects.all().first()
        old_price = prod.get_price()
        amount = float(10.00)
        # Create discount
        cat = create_discount(data)
        prod.categories.add(cat)
        # Get new Price
        new_price = prod.get_price()
        self.assertEqual(
            float(old_price.to_eng_string()),
            float(new_price.to_eng_string()) + amount
        )
