from django.core.management.base import BaseCommand
from shop.models.customer import CustomerModel
from shop.models.cart import CartModel

from django.contrib.auth.models import User

from apps.dmShipping.models import ShippingManagement

from apps.dmSquare.models import dmStockLog

from apps.dmAdvertising.models import dmAdvertisingPopup
from apps.dmAdvertising.models import dmAdvertisingTopBanner


from apps.dmRabais.models import dmRabaisPerCategory
from apps.dmRabais.models import dmPromoCode
from apps.dmRabais.models import dmCustomerPromoCode

from apps.dmBillingStripe.models import StripeOrderData

from apps.dmQuotation.models import dmQuotation

from dshop.models import Order
from dshop.models import ShippingAddress
from dshop.models import BillingAddress
from dshop.models import ProductCategory
from dshop.models import ProductFilter
from dshop.models import ProductBrand
from dshop.models import ProductLabel
from dshop.models import ProductDefault
from dshop.models import ProductVariable
from dshop.models import ProductVariableVariant
from dshop.models import Attribute
from dshop.models import AttributeValue
from dshop.models import dmSite
from dshop.models import dmSiteLogo
from dshop.models import dmSiteContact
from dshop.models import dmSiteSocial
from dshop.models import dmSiteTermsAndConditions
from dshop.models import FeatureList
from filer.models import File
from filer.models import Folder


class Command(BaseCommand):
    def handle(self, **options): # noqa
        try:
            Order.objects.all().delete()
            CustomerModel.objects.all().delete()
            CartModel.objects.all().delete()
            User.objects.all().delete()
            ShippingManagement.objects.all().delete()
            ShippingAddress.objects.all().delete()
            BillingAddress.objects.all().delete()
            ProductCategory.objects.all().delete()
            ProductFilter.objects.all().delete()
            ProductBrand.objects.all().delete()
            ProductDefault.objects.all().delete()
            ProductVariable.objects.all().delete()
            ProductVariableVariant.objects.all().delete()
            ProductLabel.objects.all().delete()
            Attribute.objects.all().delete()
            AttributeValue.objects.all().delete()
            dmRabaisPerCategory.objects.all().delete()
            dmPromoCode.objects.all().delete()
            dmCustomerPromoCode.objects.all().delete()
            dmSite.objects.all().delete()
            dmSiteLogo.objects.all().delete()
            dmSiteContact.objects.all().delete()
            dmSiteSocial.objects.all().delete()
            dmSiteTermsAndConditions.objects.all().delete()
            dmStockLog.objects.all().delete()
            StripeOrderData.objects.all().delete()
            FeatureList.objects.all().delete()
            dmAdvertisingPopup.objects.all().delete()
            dmAdvertisingTopBanner.objects.all().delete()
            File.objects.all().delete()
            Folder.objects.all().delete()
            dmQuotation.objects.all().delete()
        except Exception as e:
            print("Error from cleanning DB command: " + str(e))
