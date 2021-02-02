
from django.test import TestCase
from django.db import IntegrityError
from .utils import create_taxes
from apps.dmTaxes.models import CanadaTaxManagement

class AdvertiseModelTest(TestCase):

    def test_tax_create(self):
        create_taxes()
        self.assertEqual(1, CanadaTaxManagement.objects.all().count())

    def test_tax_update(self):
        tax = create_taxes()
        self.assertEqual(
            "Quebec",
            CanadaTaxManagement.objects.all().first().state
        )
        tax.state = "Saskatchewan"
        tax.save()
        self.assertEqual(
            "Saskatchewan",
            CanadaTaxManagement.objects.all().first().state
        )

    def test_tax_delete(self):
        tax = create_taxes()
        tax.delete()
        self.assertEqual(0, CanadaTaxManagement.objects.all().count())

    def test_tax_integrate(self):
        tax = create_taxes()
        data = {
            'state': 'Quebec',
            'hst': 2.9,
            'gst': 8,
        }
        tax_1 = create_taxes()
        self.assertEqual(IntegrityError, tax_1)
