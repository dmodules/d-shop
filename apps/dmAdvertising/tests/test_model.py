
from django.test import TestCase

from .utils import create_advertise_top_banner
from apps.dmAdvertising.models import dmAdvertisingTopBanner

class AdvertiseModelTest(TestCase):

    def test_advertising_top_banner_create(self):
        create_advertise_top_banner()
        self.assertEqual(1, dmAdvertisingTopBanner.objects.all().count())

    def test_advertising_top_banner_update(self):
        banner = create_advertise_top_banner()
        self.assertEqual(
            "Top Banner",
            dmAdvertisingTopBanner.objects.all().first().text
        )
        banner.text = "Test 123 Banner"
        banner.save()
        self.assertEqual(
            "Test 123 Banner",
            dmAdvertisingTopBanner.objects.all().first().text
        )

    def test_adverting_top_banner_delete(self):
        banner = create_advertise_top_banner()
        banner.delete()
        self.assertEqual(0, dmAdvertisingTopBanner.objects.all().count())
