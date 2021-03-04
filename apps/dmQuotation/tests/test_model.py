
from django.test import TestCase
from django.contrib.auth.models import User
from shop.models.customer import CustomerModel
from apps.dmQuotation.models import dmQuotation, dmQuotationItem

class QuotationModelTest(TestCase):

    def test_quotation_create(self):
        user = User.objects.create(
            first_name="first",
            last_name="last",
            email="first@last.test",
            username="firstlast"
        )
        customer = CustomerModel.objects.create(user=user)
        dmQuotation.objects.create(
            customer=customer,
            cookie="123",
            number='0001',
            status=1
        )
        self.assertEqual(dmQuotation.objects.all().count(), 1)

    def test_quotation_str(self):
        user = User.objects.create(
            first_name="first",
            last_name="last",
            email="first@last.test",
            username="firstlast"
        )
        customer = CustomerModel.objects.create(user=user)
        dmQuotation.objects.create(
            customer=customer,
            cookie="123",
            number='0001',
            status=1
        )
        self.assertEqual(str(dmQuotation.objects.all().first()), '0001')

    def test_quotation_item(self):
        user = User.objects.create(
            first_name="first",
            last_name="last",
            email="first@last.test",
            username="firstlast"
        )
        customer = CustomerModel.objects.create(user=user)
        q = dmQuotation.objects.create(
            customer=customer,
            cookie="123",
            number='0001',
            status=1
        )
        dmQuotationItem.objects.create(
            quotation=q,
            product_name="123",
            product_type=1,
            quantity=10
        )
        self.assertEqual(dmQuotationItem.objects.all().count(), 1)

    def test_quotation_item_str(self):
        user = User.objects.create(
            first_name="first",
            last_name="last",
            email="first@last.test",
            username="firstlast"
        )
        customer = CustomerModel.objects.create(user=user)
        q = dmQuotation.objects.create(
            customer=customer,
            cookie="123",
            number='0001',
            status=1
        )
        dmQuotationItem.objects.create(
            quotation=q,
            product_name="123",
            product_type=1,
            quantity=10
        )
        self.assertEqual(str(dmQuotationItem.objects.all().first()), '0001123')
