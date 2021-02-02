
from django.test import TestCase

from .utils import create_shipping
from apps.dmShipping.models import ShippingManagement

class ShippingModelTest(TestCase):

    def test_advertising_top_banner_create(self):
        create_shipping()
        self.assertEqual(1, ShippingManagement.objects.all().count())

    def test_advertising_top_banner_update(self):
        s_m = create_shipping()
        self.assertEqual(
            "Shipping Method",
            ShippingManagement.objects.all().first().name
        )
        s_m.name = "Shipping Method 123"
        s_m.save()
        self.assertEqual(
            "Shipping Method 123",
            ShippingManagement.objects.all().first().name
        )

    def test_adverting_top_banner_delete(self):
        s_m = create_shipping()
        s_m.delete()
        self.assertEqual(0, ShippingManagement.objects.all().count())
