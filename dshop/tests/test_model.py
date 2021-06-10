
from django.db import IntegrityError
from django.test import TestCase

from dshop.models import Product, \
    ProductCategory, \
    Attribute, \
    AttributeValue
from dshop.tests.utils import product, \
    product_variable, \
    product_variant, \
    category, \
    attribute, \
    attribute_value, \
    attach_attribute


class ProductModelTest(TestCase):

    def test_same_product(self):

        data = {
            'product_name': 'Capsicum',
            'product_code': 'caps',
            'slug': 'capsicum',
            'unit_price': 1.00,
            'quantity': 100,
            'order': 0,
            'caption': 'Capsicum'
        }
        product(None, None, data)
        # We should get integrity error
        self.assertEqual(IntegrityError, product(None, None, data))


class ProductCategoryTest(TestCase):

    def test_create_category(self):
        category()
        self.assertEqual(1,
                         ProductCategory.objects.all().count())

    def test_category_delete(self):
        cat = category()
        cat.delete()
        self.assertEqual(0,
                         ProductCategory.objects.all().count())

    def test_category_update(self):
        cat = category()
        cat.name = "123"
        cat.save()
        self.assertEqual("123",
                         ProductCategory.objects.first().name)


class ProductAttributeTest(TestCase):

    def test_attribute_create(self):
        attribute()
        self.assertEqual(1,
                         Attribute.objects.all().count())

    def test_attribute_delete(self):
        attr = attribute()
        attr.delete()
        self.assertEqual(0,
                         Attribute.objects.all().count())

    def test_attribute_update(self):
        attr = attribute()
        attr.name = '123'
        attr.save()
        self.assertEqual('123',
                         Attribute.objects.first().name)

    def test_attribute_attach_value(self):
        attr = attribute()
        values = [1, 2, 3, 4, 5]
        attribute_value(attr, values)
        self.assertEqual(len(values),
                         AttributeValue.objects.filter(attribute=attr).count())


'''class ProductBrandTest(TestCase):

    def test_create_category(self):
        product_brand()
        self.assertEqual(1,
                         ProductBrand.objects.all().count())

    def test_category_delete(self):
        brand = product_brand()
        brand.delete()
        self.assertEqual(0,
                         ProductBrand.objects.all().count())

    def test_category_update(self):
        brand = product_brand()
        brand.name = "123"
        brand.save()
        self.assertEqual("123",
                         ProductBrand.objects.first().name)
'''


class ProductVariableTest(TestCase):

    def test_variable_product_create(self):
        product_variable()
        self.assertEqual(1,
                         Product.objects.all().count())

    def test_variable_product_update(self):
        p_v = product_variable()
        p_v.product_name = "123"
        p_v.save()
        self.assertEqual("123",
                         Product.objects.first().product_name)

    def test_variable_product_delete(self):
        p_v = product_variable()
        p_v.delete()
        self.assertEqual(0,
                         Product.objects.all().count())

    def test_variant_create(self):
        p_v = product_variable()
        product_variant(p_v)
        self.assertEqual(1,
                         p_v.variants.all().count())

    def test_variant_update(self):
        p_v = product_variable()
        p_v_v = product_variant(p_v)
        p_v_v.product_code = "000xxx"
        p_v_v.save()
        self.assertEqual("000xxx",
                         p_v.variants.first().product_code)

    def test_variant_multiple(self):
        p_v = product_variable()
        product_variant(p_v)
        data = {
            'product': p_v,
            'product_code': '00002',
            'unit_price': 10,
        }
        product_variant(p_v, data)
        self.assertEqual(2,
                         p_v.variants.all().count())

    def test_variant_attribute(self):
        p_v = product_variable()
        p_v_v = product_variant(p_v)
        attr = attribute()
        values = [1]
        attr_v = attribute_value(attr, values)
        ret = attach_attribute(p_v_v, attr_v[0])
        self.assertEqual(True, ret)
