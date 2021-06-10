
import pytz
from django.test import TestCase
from datetime import datetime, timedelta

from .utils import \
    create_discount, \
    create_promo
from apps.dmRabais.models import \
    dmRabaisPerCategory, \
    dmPromoCode


class RabaisModelTest(TestCase):

    def test_category_discount_create(self):
        create_discount()
        self.assertEqual(1,
                         dmRabaisPerCategory.objects.all().count())

    def test_category_discount_str(self):
        create_discount()
        self.assertEqual("Test Discount",
                         str(dmRabaisPerCategory.objects.all().first()))

    '''def test_category_discount_duplicate(self):
        create_discount()
        create_discount()
        self.assertEqual(1,
                         dmRabaisPerCategory.objects.all().count())'''

    def test_category_discount_with_both_value(self):
        data = {
            'name': 'Test Discount',
            'amount': 10,
            'percent': 10,
            'is_active': True,
            'valid_from': pytz.utc.localize(datetime.today() - timedelta(days=2)),  # noqa
            'valid_until': pytz.utc.localize(datetime.today()),
        }

        # Record should not be created if both values are provided
        create_discount(data)
        self.assertEqual(1,
                         dmRabaisPerCategory.objects.all().count())

    def test_category_discount_edit(self):
        create_discount()
        disc = dmRabaisPerCategory.objects.all()[0]
        disc.amount = 15
        disc.save()
        self.assertEqual(15,
                         int(dmRabaisPerCategory.objects.all()[0].amount))

    def test_category_discount_delete(self):
        create_discount()
        disc = dmRabaisPerCategory.objects.all()[0]
        disc.delete()
        self.assertEqual(0,
                         dmRabaisPerCategory.objects.all().count())

    def test_promocode_create(self):
        create_promo()
        self.assertEqual(1,
                         dmPromoCode.objects.all().count())

    def test_promocode_str(self):
        create_promo()
        self.assertEqual("Test Promo",
                         str(dmPromoCode.objects.all().first()))

    def test_promocode_without_code(self):
        data = {
            'name': 'Test Promo',
            'amount': 10,
            'is_active': True,
            'valid_from': pytz.utc.localize(datetime.today()),
            'valid_until': pytz.utc.localize(datetime.today()),
        }
        create_promo(data)
        self.assertEqual(1,
                         dmPromoCode.objects.all().count())

    '''def test_promocode_duplicate(self):
        create_promo()
        create_promo()
        #There should be some validation to create duplicate promo code
        self.assertEqual(1,
                         dmPromoCode.objects.all().count())'''

    def test_promocode_with_both_value(self):
        data = {
            'name': 'Test Promo',
            'code': 'TEST50',
            'amount': 10,
            'percent': 10,
            'is_active': True,
            'valid_from': pytz.utc.localize(datetime.today()),
            'valid_until': pytz.utc.localize(datetime.today()),
        }
        create_promo(data)
        # This should not be allowed to create record with both value
        self.assertEqual(1,
                         dmPromoCode.objects.all().count())

    def test_promocode_edit(self):
        create_promo()
        promo = dmPromoCode.objects.all()[0]
        promo.amount = 15
        promo.save()
        self.assertEqual(15,
                         int(dmPromoCode.objects.all()[0].amount))

    def test_promocode_delete(self):
        create_promo()
        promo = dmPromoCode.objects.all()[0]
        promo.delete()
        self.assertEqual(0,
                         dmPromoCode.objects.all().count())
