
from django.test import TestCase
from datetime import datetime

from dshop.models import ProductCategory
from apps.dmRabais.models import dmRabaisPerCategory, \
    dmPromoCode


class RabaisModelTest(TestCase):

    def setUp(self):
        self.create_category()

    def create_category(self):
        data = {
            'name': 'category_1',
            'order': 1
        }
        ProductCategory.objects.create(**data)

    def create_discount(self, data):
        if not data:
            return None

        try:
            drpc = dmRabaisPerCategory.objects.create(**data)
            cat = ProductCategory.objects.all()[0]
            drpc.categories.add(cat)
        except Exception as e:
            print(e)
            return False
        return True

    def create_promo(self, data):
        if not data:
            return None

        try:
            dmPromoCode.objects.create(**data)
        except Exception as e:
            print(e)
            return False
        return True

    def test_category_discount_create(self):
        data = {
            'name': 'Test Discount',
            'amount': 10,
            'is_active': True,
            'valid_from': datetime.today(),
            'valid_until': datetime.today(),
        }
        self.create_discount(data)
        self.assertEqual(1,
                         dmRabaisPerCategory.objects.all().count())

    '''def test_category_discount_duplicate(self):
        data = {
            'name': 'Test Discount',
            'amount': 10,
            'is_active': True,
            'valid_from': datetime.today(),
            'valid_until': datetime.today(),
        }
        self.create_discount(data)
        self.create_discount(data)
        self.assertEqual(1,
                         dmRabaisPerCategory.objects.all().count())'''

    def test_category_discount_with_both_value(self):
        data = {
            'name': 'Test Discount',
            'amount': 10,
            'percent': 10,
            'is_active': True,
            'valid_from': datetime.today(),
            'valid_until': datetime.today(),
        }
        # Record should not be created if both values are provided
        self.create_discount(data)
        self.assertEqual(1,
                         dmRabaisPerCategory.objects.all().count())

    def test_category_discount_edit(self):
        data = {
            'name': 'Test Discount',
            'amount': 10,
            'is_active': True,
            'valid_from': datetime.today(),
            'valid_until': datetime.today(),
        }
        self.create_discount(data)
        disc = dmRabaisPerCategory.objects.all()[0]
        disc.amount = 15
        disc.save()
        self.assertEqual(15,
                         int(dmRabaisPerCategory.objects.all()[0].amount))

    def test_category_discount_delete(self):
        data = {
            'name': 'Test Discount',
            'amount': 10,
            'is_active': True,
            'valid_from': datetime.today(),
            'valid_until': datetime.today(),
        }
        self.create_discount(data)
        disc = dmRabaisPerCategory.objects.all()[0]
        disc.delete()
        self.assertEqual(0,
                         dmRabaisPerCategory.objects.all().count())

    def test_promocode_create(self):
        data = {
            'name': 'Test Promo',
            'code': 'TEST50',
            'amount': 10,
            'is_active': True,
            'valid_from': datetime.today(),
            'valid_until': datetime.today(),
        }
        self.create_promo(data)
        self.assertEqual(1,
                         dmPromoCode.objects.all().count())

    '''def test_promocode_duplicate(self):
        data = {
            'name': 'Test Promo',
            'code': 'TEST50',
            'amount': 10,
            'is_active': True,
            'valid_from': datetime.today(),
            'valid_until': datetime.today(),
        }
        self.create_promo(data)
        self.create_promo(data)
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
            'valid_from': datetime.today(),
            'valid_until': datetime.today(),
        }
        self.create_promo(data)
        # This should not be allowed to create record with both value
        self.assertEqual(1,
                         dmPromoCode.objects.all().count())

    def test_promocode_edit(self):
        data = {
            'name': 'Test Promo',
            'code': 'TEST50',
            'amount': 10,
            'is_active': True,
            'valid_from': datetime.today(),
            'valid_until': datetime.today(),
        }
        self.create_promo(data)
        promo = dmPromoCode.objects.all()[0]
        promo.amount = 15
        promo.save()
        self.assertEqual(15,
                         int(dmPromoCode.objects.all()[0].amount))

    def test_promocode_delete(self):
        data = {
            'name': 'Test Promo',
            'code': 'TEST50',
            'amount': 10,
            'is_active': True,
            'valid_from': datetime.today(),
            'valid_until': datetime.today(),
        }
        self.create_promo(data)
        promo = dmPromoCode.objects.all()[0]
        promo.delete()
        self.assertEqual(0,
                         dmPromoCode.objects.all().count())
