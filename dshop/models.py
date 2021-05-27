import re
import pytz

from mptt.models import MPTTModel, TreeForeignKey

from decimal import Decimal
from datetime import datetime
from cms.models import CMSPlugin
from colorfield.fields import ColorField
from polymorphic.query import PolymorphicQuerySet

from cms.models import Page

from filer.fields import image
from filer.fields.file import FilerFileField

from parler.fields import TranslatedField
from parler.managers import TranslatableManager, TranslatableQuerySet
from parler.models import TranslatableModel, TranslatableModelMixin
from parler.models import TranslatedFieldsModel, TranslatedFields

from django.db import models
from django.db.models import Q
from django.contrib import sites
from django.core.validators import MinValueValidator
from djangocms_text_ckeditor.fields import HTMLField
from django.utils.six.moves.urllib.parse import urljoin
from django.utils.translation import ugettext_lazy as _
from autoslug import AutoSlugField
from django.utils.translation import get_language_from_request

from shop.money import Money, MoneyMaker
from shop.money.fields import MoneyField
from shop.models.address import BaseShippingAddress, BaseBillingAddress
from shop.models.customer import CustomerModel
from shop.models.defaults.cart import Cart
from shop.models.defaults.cart_item import CartItem
from shop.models.defaults.customer import Customer
from shop.models.defaults.mapping import ProductPage, ProductImage
from shop.models.defaults.order import Order
from shop.models.fields import JSONField
from shop.models.order import BaseOrderItem
from shop.models.product import BaseProduct, BaseProductManager
from shop.models.product import AvailableProductMixin

from .utils import get_apply_discountpercategory
from shop.models.delivery import BaseDelivery, BaseDeliveryItem


try:
    from apps.dmRabais.models import dmRabaisPerCategory
    from apps.dmRabais.models import dmPromoCode
    from apps.dmRabais.models import dmCustomerPromoCode
except Exception as e:
    print(e)
    dmRabaisPerCategory = None
    dmPromoCode = None
    dmCustomerPromoCode = None

__all__ = ["Cart", "CartItem", "Order", "Customer"]

TAG_RE = re.compile(r"<[^>]+>")


class Delivery(BaseDelivery):
    class Meta:
        get_latest_by = ["pk"]


class DeliveryItem(BaseDeliveryItem):
    quantity = models.PositiveIntegerField(
        _("Ordered Quantity")
    )

    class Meta:
        get_latest_by = ["pk"]


class OrderItem(BaseOrderItem):
    quantity = models.PositiveIntegerField(
        _("Ordered Quantity")
    )
    variables = JSONField(
        verbose_name=_("Data")
    )

    canceled = models.BooleanField(
        verbose_name=_("Canceled"),
        default=False
    )

    def populate_from_cart_item(self, cart_item, request):
        super().populate_from_cart_item(cart_item, request)
        self.variables = cart_item.extra
        self.save()


class CMSPageReferenceMixin(object):
    category_fields = ["cms_pages"]

    def get_absolute_url(self):
        page = Page.objects.filter(reverse_id="produits").first()
        if page is not None:
            return page.get_absolute_url()
        return ""


class ProductQuerySet(TranslatableQuerySet, PolymorphicQuerySet):
    pass


class ProductManager(BaseProductManager, TranslatableManager):
    queryset_class = ProductQuerySet

    def get_queryset(self):
        qs = self.queryset_class(self.model, using=self._db)
        return qs.prefetch_related("translations")


#######################################################################
# Adresses
#######################################################################

COUNTRIES_FR = [
    ('AF', _('Afghanistan')), ('ZA', _('Afrique du Sud')),
    ('AL', _('Albanie')), ('DZ', _('Algérie')),
    ('DE', _('Allemagne')), ('AD', _('Andorre')),
    ('AO', _('Angola')), ('AG', _('Antigua-et-Barbuda')),
    ('SA', _('Arabie saoudite')), ('AR', _('Argentine')),
    ('AM', _('Arménie')), ('AU', _('Australie')),
    ('AT', _('Autriche')), ('AZ', _('Azerbaïdjan')),
    ('BS', _('Bahamas')), ('BH', _('Bahreïn')),
    ('BD', _('Bangladesh')), ('BB', _('Barbade')),
    ('BY', _('Biélorussie')), ('BE', _('Belgique')),
    ('BZ', _('Belize')), ('BJ', _('Bénin')), ('BT', _('Bhoutan')),
    ('BO', _('Bolivie')), ('BA', _('Bosnie-Herzégovine')),
    ('BW', _('Botswana')), ('BR', _('Brésil')),
    ('BN', _('Brunei')), ('BG', _('Bulgarie')),
    ('BF', _('Burkina Faso')), ('BI', _('Burundi')),
    ('KH', _('Cambodge')), ('CM', _('Cameroun')),
    ('CA', _('Canada')), ('CV', _('Cap-Vert')),
    ('CF', _('République centrafricaine')), ('CL', _('Chili')),
    ('CN', _('Chine')), ('CY', _('Chypre (pays)')),
    ('CO', _('Colombie')), ('KM', _('Comores (pays)')),
    ('CG', _('République du Congo')),
    ('CD', _('République démocratique du Congo')),
    ('KR', _('Corée du Sud')), ('KP', _('Corée du Nord')),
    ('CR', _('Costa Rica')), ('CI', _("Côte d'Ivoire")),
    ('HR', _('Croatie')), ('CU', _('Cuba')), ('DK', _('Danemark')),
    ('DJ', _('Djibouti')), ('DO', _('République dominicaine')),
    ('DM', _('Dominique')), ('EG', _('Égypte')),
    ('SV', _('Salvador')), ('AE', _('Émirats arabes unis')),
    ('EC', _('Équateur (pays)')), ('ER', _('Érythrée')),
    ('ES', _('Espagne')), ('EE', _('Estonie')),
    ('US', _('États-Unis')), ('ET', _('Éthiopie')),
    ('FJ', _('Fidji')), ('FI', _('Finlande')), ('FR', _('France')),
    ('GA', _('Gabon')), ('GM', _('Gambie')),
    ('GE', _('Géorgie (pays)')), ('GH', _('Ghana')),
    ('GR', _('Grèce')), ('GD', _('Grenade (pays)')),
    ('GT', _('Guatemala')), ('GN', _('Guinée')),
    ('GW', _('Guinée-Bissau')), ('GQ', _('Guinée équatoriale')),
    ('GY', _('Guyana')), ('HT', _('Haïti')), ('HN', _('Honduras')),
    ('HU', _('Hongrie')),
    ('IN', _('Inde')), ('ID', _('Indonésie')), ('IR', _('Iran')),
    ('IQ', _('Irak')), ('IE', _('Irlande (pays)')),
    ('IS', _('Islande')), ('IL', _('Israël')), ('IT', _('Italie')),
    ('JM', _('Jamaïque')),
    ('JP', _('Japon')), ('JO', _('Jordanie')),
    ('KZ', _('Kazakhstan')), ('KE', _('Kenya')),
    ('KG', _('Kirghizistan')), ('KI', _('Kiribati')),
    ('KW', _('Koweït')), ('LA', _('Laos')), ('LS', _('Lesotho')),
    ('LV', _('Lettonie')), ('LB', _('Liban')),
    ('LR', _('Liberia')), ('LY', _('Libye')),
    ('LI', _('Liechtenstein')), ('LT', _('Lituanie')),
    ('LU', _('Luxembourg (pays)')), ('MK', _('Macédoine du Nord')),
    ('MG', _('Madagascar')), ('MY', _('Malaisie')),
    ('MW', _('Malawi')), ('MV', _('Maldives')), ('ML', _('Mali')),
    ('MT', _('Malte')), ('MA', _('Maroc')),
    ('MH', _('Îles Marshall (pays)')), ('MU', _('Maurice (pays)')),
    ('MR', _('Mauritanie')), ('MX', _('Mexique')),
    ('FM', _('États fédérés de Micronésie (pays)')),
    ('MD', _('Moldavie')), ('MC', _('Monaco')),
    ('MN', _('Mongolie')), ('ME', _('Monténégro')),
    ('MZ', _('Mozambique')), ('MM', _('Birmanie')),
    ('NA', _('Namibie')), ('NR', _('Nauru')), ('NP', _('Népal')),
    ('NI', _('Nicaragua')), ('NE', _('Niger')), ('NG', _('Nigeria')),
    ('NO', _('Norvège')), ('NZ', _('Nouvelle-Zélande')),
    ('OM', _('Oman')), ('UG', _('Ouganda')),
    ('UZ', _('Ouzbékistan')), ('PK', _('Pakistan')),
    ('PW', _('Palaos')), ('PA', _('Panama')),
    ('PG', _('Papouasie-Nouvelle-Guinée')), ('PY', _('Paraguay')),
    ('NL', _('Pays-Bas')), ('PE', _('Pérou')),
    ('PH', _('Philippines')), ('PL', _('Pologne')),
    ('PT', _('Portugal')), ('QA', _('Qatar')), ('RO', _('Roumanie')),
    ('GB', _('Royaume-Uni')), ('RU', _('Russie')),
    ('RW', _('Rwanda')), ('KN', _('Saint-Christophe-et-Niévès')),
    ('SM', _('Saint-Marin')),
    ('VC', _('Saint-Vincent-et-les-Grenadines')),
    ('LC', _('Sainte-Lucie')), ('SB', _('Salomon')),
    ('WS', _('Samoa')), ('ST', _('Sao Tomé-et-Principe')),
    ('SN', _('Sénégal')), ('RS', _('Serbie')),
    ('SC', _('Seychelles')), ('SL', _('Sierra Leone')),
    ('SG', _('Singapour')), ('SK', _('Slovaquie')),
    ('SI', _('Slovénie')), ('SO', _('Somalie')), ('SD', _('Soudan')),
    ('SS', _('Soudan du Sud')), ('LK', _('Sri Lanka')),
    ('SE', _('Suède')), ('CH', _('Suisse')), ('SR', _('Suriname')),
    ('SZ', _('Eswatini')), ('SY', _('Syrie')),
    ('TJ', _('Tadjikistan')), ('TZ', _('Tanzanie')),
    ('TD', _('Tchad')), ('CZ', _('Tchéquie')),
    ('TH', _('Thaïlande')), ('TL', _('Timor oriental')),
    ('TG', _('Togo')), ('TO', _('Tonga')),
    ('TT', _('Trinité-et-Tobago')), ('TN', _('Tunisie')),
    ('TM', _('Turkménistan')), ('TR', _('Turquie')),
    ('TV', _('Tuvalu')), ('UA', _('Ukraine')), ('UY', _('Uruguay')),
    ('VU', _('Vanuatu')), ('VE', _('Venezuela')),
    ('VN', _('Viêt Nam')), ('YE', _('Yémen')), ('ZM', _('Zambie')),
    ('ZW', _('Zimbabwe'))
]


class ShippingAddress(BaseShippingAddress):
    """
    Customer's shipping address.
    """

    name = models.CharField(
        _("Fullname"),
        max_length=1024
    )
    address1 = models.CharField(
        _("Address 1"),
        max_length=1024
    )
    address2 = models.CharField(
        _("Address 2"),
        max_length=1024,
        blank=True,
        null=True
    )
    country = models.CharField(
        _("Country"),
        max_length=4
    )
    province = models.CharField(
        _("Province / State"),
        max_length=1024
    )
    city = models.CharField(
        _("City"),
        max_length=1024
    )
    zip_code = models.CharField(
        _("Postal Code"),
        max_length=255
    )

    class Meta:
        verbose_name = _("Shipping Address")
        verbose_name_plural = _("Shipping Addresses")

    def get_country_display(self):
        result = self.country
        for item in COUNTRIES_FR:
            if self.country in item[0]:
                result = item[1]
        return result


class BillingAddress(BaseBillingAddress):
    """
    Customer's billing address.
    """

    name = models.CharField(
        _("Fullname"),
        max_length=1024
    )
    address1 = models.CharField(
        _("Address 1"),
        max_length=1024
    )
    address2 = models.CharField(
        _("Address 2"),
        max_length=1024,
        blank=True,
        null=True
    )
    country = models.CharField(
        _("Country"),
        max_length=4
    )
    province = models.CharField(
        _("Province / State"),
        max_length=1024
    )
    city = models.CharField(
        _("City"),
        max_length=1024
    )
    zip_code = models.CharField(
        _("Postal Code"),
        max_length=255
    )

    class Meta:
        verbose_name = _("Billing Address")
        verbose_name_plural = _("Billing Addresses")

    def get_country_display(self):
        result = self.country
        for item in COUNTRIES_FR:
            if self.country in item[0]:
                result = item[1]
        return result


#######################################################################
# Produit: Catégorie/Filtres
#######################################################################

class ProductCategory(CMSPageReferenceMixin, MPTTModel):
    """
    A model to help to categorize products.
    Product can have multiple categories.
    """

    CHOIX_POS = [
        (1, _("Left")),
        (2, _("Center")),
        (3, _("Right"))
    ]

    name = models.CharField(
        verbose_name=_("Category's Name"),
        max_length=100,
        null=False,
        blank=False
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        verbose_name=_("Parent's Category"),
        related_name='children',
        blank=True,
        null=True
    )
    square_id = models.CharField(
        verbose_name=_("Square ID"),
        max_length=30,
        null=True,
        blank=True
    )
    order = models.PositiveSmallIntegerField(
        verbose_name=_("Sort by"),
        default=0,
        blank=False,
        null=False
    )
    text = HTMLField(
        verbose_name=_("Text"),
        configuration="CKEDITOR_SETTINGS_DMPLUGIN",
        null=True,
        blank=True,
        help_text=_("A text that will be shown on the top of the page of the Products of this category.")
    )
    text_position = models.PositiveSmallIntegerField(
        verbose_name=_("Position"),
        choices=CHOIX_POS,
        default=1,
        help_text=_("Position of the text.")
    )
    text_color = ColorField(
        verbose_name=_("Text's Colour"),
        null=True,
        blank=True
    )
    bg_color = ColorField(
        verbose_name=_("Background's Colour"),
        null=True,
        blank=True
    )
    image = image.FilerImageField(
        verbose_name=_("Header's Image"),
        on_delete=models.SET_NULL,
        related_name="category_image",
        null=True,
        blank=True,
        help_text=_("An image that will be shown on the top of the page of the Products of this category.")
    )

    active = models.BooleanField(default=True,
                                 verbose_name=_("Active"),)

    class Meta:
        verbose_name = _("Product's Category")
        verbose_name_plural = _("Product's Categories")

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    def __str__(self):
        if self.parent is not None:
            if self.parent.parent is not None:
                return self.parent.parent.name + " | " + self.parent.name + " | " + self.name
            else:
                return self.parent.name + " | " + self.name
        else:
            return self.name

    def get_products(self):
        result = Product.objects.filter(
            Q(categories=self) | Q(categories__parent=self)
            | Q(categories__parent__parent=self)
            | Q(categories__parent__parent__parent=self),
            active=True).order_by("id")
        return result

    def get_absolute_url(self):
        name = "-".join(self.name.lower().split(' '))
        if self.get_current_language() == "en":
            return urljoin("/en/products/category/", str(self.id) + '-' + name)
        return urljoin("/fr/produits/category/", str(self.id) + '-' + name)


class ProductFilterGroup(TranslatableModel):

    name = models.CharField(
        verbose_name=_("Filter's Group Name"),
        max_length=100,
        null=False,
        blank=False
    )
    name_trans = TranslatedField()
    order = models.PositiveSmallIntegerField(
        verbose_name=_("Sort by"),
        default=0,
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = _("Product's Filter Group")
        verbose_name_plural = _("Product's Filter Groups")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class ProductFilterGroupTranslation(TranslatedFieldsModel):
    """
    A model to handle translations of ProductFilterGroup
    """

    master = models.ForeignKey(
        ProductFilterGroup,
        on_delete=models.CASCADE,
        related_name="translations",
        null=True
    )
    name_trans = models.CharField(
        verbose_name=_("Translated Filter's Group Name"),
        max_length=100,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = [("language_code", "master")]


class ProductFilter(TranslatableModel):
    """
    A model to help to filter products.
    Product can have multiple filters.
    """
    group = models.ForeignKey(
        ProductFilterGroup,
        on_delete=models.SET_NULL,
        verbose_name=_("Filter Group"),
        blank=True,
        null=True,
        help_text=_("Add a group to Filter.")
    )
    name = models.CharField(
        verbose_name=_("Filter's Name"),
        max_length=100,
        null=False,
        blank=False
    )
    name_trans = TranslatedField()
    image = image.FilerImageField(
        verbose_name=_("image"),
        related_name="filter_image",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    order = models.PositiveSmallIntegerField(
        verbose_name=_("Sort by"),
        default=0,
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = _("Product's Filter")
        verbose_name_plural = _("Product's Filters")
        ordering = ["group", "order", "-pk"]

    def __str__(self):
        if self.group:
            return self.group.name + " : " + self.name
        return self.name


class ProductFilterTranslation(TranslatedFieldsModel):
    """
    A model to handle translations of ProductFilter
    """

    master = models.ForeignKey(
        ProductFilter,
        on_delete=models.CASCADE,
        related_name="translations",
        null=True
    )
    name_trans = models.CharField(
        verbose_name=_("Translated Filter's Name"),
        max_length=100,
        null=True,
        blank=True
    )
    description = models.TextField(
        null=True, blank=True
    )

    class Meta:
        unique_together = [("language_code", "master")]


class ProductBrand(models.Model):
    """
    A model to help to brands products.
    Product can only have one brand.
    """

    name = models.CharField(
        verbose_name=_("Brand's Name"),
        max_length=100,
        null=False,
        blank=False
    )
    logo = image.FilerImageField(
        verbose_name=_("Logo"),
        related_name="brand_logo",
        on_delete=models.CASCADE
    )
    order = models.PositiveSmallIntegerField(
        verbose_name=_("Sort by"),
        default=0,
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = _("Product's Brand")
        verbose_name_plural = _("Product's Brands")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def get_products(self):
        result = Product.objects.filter(
            brand=self,
            active=True
        ).order_by("id")
        return result


class ProductLabel(models.Model):
    """
    A model to add a custom label
    on product's media.
    """

    name = models.CharField(
        verbose_name=_("Label's Name"),
        max_length=25,
        null=False,
        blank=False,
        help_text=_("Maximum 25 characters.")
    )
    colour = ColorField(
        verbose_name=_("Text's Colour"),
        default="#000",
        null=False,
        blank=False
    )
    bg_colour = ColorField(
        verbose_name=_("Background's Colour"),
        default="#fff",
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = _("Product's Label")
        verbose_name_plural = _("Product's Labels")
        ordering = ["name"]

    def __str__(self):
        return self.name


#######################################################################
# Produits
#######################################################################


class Product(CMSPageReferenceMixin, TranslatableModelMixin, BaseProduct):
    """
    A basic model to handle polymorphic Product
    """
    product_name = models.CharField(
        _("Product's Name"),
        max_length=255
    )
    slug = AutoSlugField(
        populate_from="product_name",
        unique=True
    )
    categories = models.ManyToManyField(
        ProductCategory,
        verbose_name=_("Categories"),
        blank=True
    )
    filters = models.ManyToManyField(
        ProductFilter,
        verbose_name=_("Filters"),
        blank=True
    )
    brand = models.ForeignKey(
        ProductBrand,
        on_delete=models.SET_NULL,
        verbose_name=_("Brand"),
        blank=True,
        null=True
    )
    label = models.ForeignKey(
        ProductLabel,
        on_delete=models.SET_NULL,
        verbose_name=_("Custom Label"),
        blank=True,
        null=True,
        help_text=_("Add a custom label to the product.")
    )
    is_vedette = models.BooleanField(
        _("Featured"),
        default=False
    )
    caption = TranslatedField()
    description = TranslatedField()
    order = models.PositiveIntegerField(
        _("Sort by"),
        db_index=True
    )
    cms_pages = models.ManyToManyField(
        "cms.Page",
        through=ProductPage
    )
    main_image = image.FilerImageField(
        verbose_name=_("Main Image"),
        on_delete=models.SET_NULL,
        related_name="main_image",
        null=True,
        blank=True
    )
    images = models.ManyToManyField(
        "filer.Image",
        through=ProductImage
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["order"]

    objects = ProductManager()

    lookup_fields = ["product_name__icontains", "description__icontains"]

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        page = Page.objects.filter(reverse_id="produits").first()
        if page is not None:
            return urljoin(page.get_absolute_url(), self.slug)
        return ""

    @property
    def sample_image(self):
        if self.main_image:
            return self.main_image
        else:
            return self.images.first()


class ProductTranslation(TranslatedFieldsModel):
    """
    A model to handle translations of Product
    """

    master = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="translations",
        null=True
    )
    caption = HTMLField(
        verbose_name=_("Caption"),
        configuration="CKEDITOR_SETTINGS_CAPTION",
        blank=True,
        null=True,
        help_text=_("Short description.")
    )
    description = HTMLField(
        verbose_name=_("Description"),
        configuration="CKEDITOR_SETTINGS_DESCRIPTION",
        blank=True,
        null=True,
        help_text=_("Long description."),
    )

    class Meta:
        unique_together = [("language_code", "master")]


# ===---


class ProductDefault(AvailableProductMixin, Product):
    """
    A basic Product, polymorphic child of Product
    """

    product_code = models.CharField(
        _("Product's Code"),
        max_length=255,
        unique=True,
        help_text=_("A unique code.")
    )
    unit_price = MoneyField(
        _("Unit Price"),
        decimal_places=3,
        help_text=_("Net price for this product.")
    )
    quantity = models.PositiveIntegerField(
        _("Quantity"),
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_("Available quantity in stock.")
    )
    multilingual = TranslatedFields(
        description=HTMLField(
            verbose_name=_("Description"),
            configuration="CKEDITOR_SETTINGS_DESCRIPTION",
            help_text=_("Long description.")
        )
    )
    discounted_price = MoneyField(
        _("Discounted Unit Price"),
        decimal_places=3,
        null=True,
        blank=True,
        default=0,
        help_text=_("Net discounted price for this product.")
    )
    start_date = models.DateTimeField(
        _("Discount Start DateTime"),
        null=True,
        blank=True,
        help_text=_("Start DateTime Discount"),
    )
    end_date = models.DateTimeField(
        _("Discount Stop DateTime"),
        null=True,
        blank=True,
        help_text=_("Stop DateTime Discount"),
    )

    class Meta:
        verbose_name = _("Default Product")
        verbose_name_plural = _("Default Products")

    @property
    def get_caption(self):
        if self.caption:
            c = TAG_RE.sub("", self.caption)
            return c
        return ""

    @property
    def get_description(self):
        if self.description:
            desc = TAG_RE.sub("", self.description)
            return desc
        return ""

    @property
    def is_discounted(self):
        if self.discounted_price == Money(0) or \
           self.discounted_price is None or \
           self.start_date is None or \
           self.end_date is None:
            return False
        today = pytz.utc.localize(datetime.utcnow())
        if self.start_date < today and self.end_date > today:
            return True
        return False

    def get_price(self, request=None):  # noqa C910
        r = self.unit_price

        if self.is_discounted:
            r = self.discounted_price

        # ===--- GET DISCOUNTS
        if dmRabaisPerCategory is not None:
            r = get_apply_discountpercategory(self, r, self.is_discounted)

        if request:
            # ===--- GET PROMOCODE
            if dmPromoCode is not None:
                try:
                    customer = CustomerModel.objects.get_from_request(request)
                    today = pytz.utc.localize(datetime.utcnow())
                    all_codes = dmCustomerPromoCode.objects.filter(
                        (
                            Q(promocode__categories=None) | Q(promocode__categories__in=self.categories.all())
                        ) & (
                            Q(promocode__products=None) | Q(promocode__products__in=[self])
                        ) & Q(promocode__is_active=True) & (
                            Q(promocode__valid_from__isnull=True) | Q(promocode__valid_from__lte=today)
                        ) & (
                            Q(promocode__valid_until__isnull=True) | Q(promocode__valid_until__gt=today)
                        ) & Q(promocode__apply_on_cart=False),
                        customer=customer,
                        is_expired=False
                    ).distinct()
                    if all_codes.count() > 0:
                        for d in all_codes:
                            if not self.is_discounted or (
                                self.is_discounted and d.promocode.can_apply_on_discounted
                            ):
                                if d.promocode.amount is not None:
                                    r = Money(Decimal(r) - Decimal(d.promocode.amount))
                                elif d.promocode.percent is not None:
                                    pourcent = Decimal(
                                        d.promocode.percent) / Decimal("100")
                                    discount = Money(
                                        Decimal(self.unit_price) * pourcent)
                                    r = r - discount
                except Exception:
                    print("Error on ProductDefault's get_price")
        if Decimal(r) <= 0:
            r = Money(0)
        return r

    def get_promocodes(self, request):
        if dmPromoCode:
            customer = CustomerModel.objects.get_from_request(request)
            today = pytz.utc.localize(datetime.utcnow())
            if self.is_discounted:
                all_codes = dmCustomerPromoCode.objects.filter(
                    (
                        Q(promocode__categories=None) | Q(promocode__categories__in=self.categories.all())
                    ) & (
                        Q(promocode__products=None) | Q(promocode__products__in=[self])
                    )
                    & Q(promocode__is_active=True) & (
                        Q(promocode__valid_from__isnull=True) | Q(promocode__valid_from__lte=today)
                    ) & (Q(promocode__valid_until__isnull=True) | Q(promocode__valid_until__gt=today))
                    & Q(promocode__can_apply_on_discounted=True),
                    customer=customer,
                    is_expired=False
                ).distinct()
            else:
                all_codes = dmCustomerPromoCode.objects.filter(
                    (
                        Q(promocode__categories=None) | Q(promocode__categories__in=self.categories.all())
                    ) & (
                        Q(promocode__products=None) | Q(promocode__products__in=[self])
                    )
                    & Q(promocode__is_active=True) & (
                        Q(promocode__valid_from__isnull=True) | Q(promocode__valid_from__lte=today)
                    ) & (Q(promocode__valid_until__isnull=True) | Q(promocode__valid_until__gt=today)),
                    customer=customer,
                    is_expired=False
                ).distinct()
            return all_codes

    def get_realprice(self):
        return self.unit_price


# ===---


class ProductVariable(Product):
    """
    A basic variable Product, polymorphic child of Product,
    parent of ProductVariableVariant.
    """
    square_id = models.CharField(
        verbose_name=_("Square ID"),
        max_length=30,
        null=True,
        blank=True
    )
    multilingual = TranslatedFields(
        description=HTMLField(
            verbose_name=_("Description"),
            configuration="CKEDITOR_SETTINGS_DESCRIPTION",
            help_text=_("Long description.")
        )
    )

    class Meta:
        verbose_name = _("Variable Product")
        verbose_name_plural = _("Variable Products")

    default_manager = ProductManager()

    @property
    def get_caption(self):
        if self.caption:
            c = TAG_RE.sub("", self.caption)
            return c
        return ""

    @property
    def get_description(self):
        if self.description:
            desc = TAG_RE.sub("", self.description)
            return desc
        return ""

    def get_price(self, request=None):
        if not hasattr(self, "_price"):
            if self.variants.exists():
                currency = self.variants.first().unit_price.currency
                aggr = self.variants.aggregate(models.Min("unit_price"))
                self._price = MoneyMaker(currency)(aggr["unit_price__min"])
            else:
                self._price = Money()
        return self._price

    def get_availability(self, request, **kwargs):
        variant = self.get_product_variant(**kwargs)
        return variant.get_availability(request)

    def deduct_from_stock(self, quantity, **kwargs):
        variant = self.get_product_variant(**kwargs)
        variant.deduct_from_stock(quantity)

    def is_in_cart(self, cart, watched=False, **kwargs):
        try:
            product_code = kwargs["product_code"]
        except KeyError:
            return
        cart_item_qs = CartItem.objects.filter(cart=cart, product=self)
        for cart_item in cart_item_qs:
            if cart_item.product_code == product_code:
                return cart_item

    def get_product_variant(self, **kwargs):
        try:
            product_code = kwargs.get("product_code")
            return self.variants.get(product_code=product_code)
        except ProductVariableVariant.DoesNotExist as e:
            raise ProductVariable.DoesNotExist(e)

    def get_product_variants(self):
        return self.variants.all()

    def get_product_attribute(self):
        if self.variants.all():
            data = {}
            for a in self.variants.all()[0].attribute.all():
                if a.attribute.name not in data:
                    data[a.attribute.name] = []
            for d in data:
                data[d] = list(AttributeValue.objects.filter(attribute__name=d).values_list('value', flat=True))
            return data

    def get_attribute_values(self):
        if self.variants.all():
            data = {}
            data["key"] = []
            data["value"] = []
            for v in self.variants.all():
                for a in v.attribute.all():
                    if a.attribute.name not in data["key"]:
                        data["key"].append(a.attribute.name)
                    if a.value not in data["value"]:
                        data["value"].append(a.value)
            return data


class Attribute(models.Model):
    name = models.CharField(
        _("Attribute Name"),
        max_length=250,
        help_text=_("Attribute Name")
    )
    square_id = models.CharField(
        verbose_name=_("Square ID"),
        max_length=30,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _("Product's Attribute")
        verbose_name_plural = _("Product's Attributes")

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        verbose_name=_("Attribute"),
        related_name="attribute"
    )
    square_id = models.CharField(
        verbose_name=_("Square ID"),
        max_length=30,
        null=True,
        blank=True
    )
    value = models.CharField(
        _("Attribute Value"),
        max_length=250,
        help_text=_("Attribute Value")
    )

    def __str__(self):
        return self.attribute.name + ' - ' + self.value


class ProductVariableVariant(AvailableProductMixin, models.Model):
    """
    A basic variant of ProductVariable, will be used to populate
    cart item data.
    """

    product = models.ForeignKey(
        ProductVariable,
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
        related_name="variants"
    )
    product_code = models.CharField(
        _("Product's Code"),
        max_length=255,
        unique=True
    )
    attribute = models.ManyToManyField(
        AttributeValue,
        verbose_name=_("Attribute"),
        blank=True
    )
    unit_price = MoneyField(
        _("Unit Price"),
        decimal_places=3,
        help_text=_("Net price for this product.")
    )
    quantity = models.PositiveIntegerField(
        _("Quantity"),
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_("Available quantity in stock.")
    )
    discounted_price = MoneyField(
        _("Discounted Unit Price"),
        decimal_places=3,
        null=True,
        blank=True,
        default=0,
        help_text=_("Net discounted price for this product.")
    )
    start_date = models.DateTimeField(
        _("Discount Start DateTime"),
        null=True,
        blank=True,
        help_text=_("Start DateTime Discount"),
    )
    end_date = models.DateTimeField(
        _("Discount Stop DateTime"),
        null=True,
        blank=True,
        help_text=_("Stop DateTime Discount"),
    )
    variant_image = image.FilerImageField(
        verbose_name=_("Variant Image"),
        on_delete=models.SET_NULL,
        related_name="variant_image",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _("Product Variant")
        verbose_name_plural = _("Product Variants")

    def __str__(self):
        return _("{product}").format(product=self.product)

    @property
    def is_discounted(self):
        if self.discounted_price == Money(0) or self.discounted_price is None:
            return False
        today = pytz.utc.localize(datetime.utcnow())
        if not self.start_date:
            return False
        if self.start_date < today and not self.end_date:
            return True
        elif self.start_date < today and self.end_date > today:
            return True

    def get_price(self, request=None):  # noqa: C901
        r = self.unit_price

        if self.is_discounted:
            r = self.discounted_price

        # ===--- GET DISCOUNTS
        if dmRabaisPerCategory is not None:
            r = get_apply_discountpercategory(self.product, r, self.is_discounted)

        if request:
            # ===--- GET PROMOCODE
            if dmPromoCode is not None:
                try:
                    customer = CustomerModel.objects.get_from_request(request)
                    today = pytz.utc.localize(datetime.utcnow())
                    all_codes = dmCustomerPromoCode.objects.filter(
                        (
                            Q(promocode__categories=None) | Q(promocode__categories__in=self.product.categories.all())
                        ) & (
                            Q(promocode__products=None) | Q(promocode__products__in=[self.product])
                        ) & Q(promocode__is_active=True) & (
                            Q(promocode__valid_from__isnull=True) | Q(promocode__valid_from__lte=today)
                        ) & (
                            Q(promocode__valid_until__isnull=True) | Q(promocode__valid_until__gt=today)
                        ) & Q(promocode__apply_on_cart=False),
                        customer=customer,
                        is_expired=False
                    ).distinct()
                    if all_codes.count() > 0:
                        for d in all_codes:
                            if not self.is_discounted or (
                                self.is_discounted and d.promocode.can_apply_on_discounted
                            ):
                                if d.promocode.amount is not None:
                                    r = Money(Decimal(r) - Decimal(d.promocode.amount))
                                elif d.promocode.percent is not None:
                                    pourcent = Decimal(d.promocode.percent) / Decimal("100")
                                    discount = Money(Decimal(self.unit_price) * pourcent)
                                    r = r - discount
                except Exception:
                    print("Error on ProductVariableVariant's get_price")
        if Decimal(r) <= 0:
            r = Money(0)
        return r

    def get_promocodes(self, request):
        if dmPromoCode is not None:
            customer = CustomerModel.objects.get_from_request(request)
            today = pytz.utc.localize(datetime.utcnow())
            all_codes = dmCustomerPromoCode.objects.filter(
                (
                    Q(promocode__categories=None) | Q(promocode__categories__in=self.product.categories.all())
                ) & (
                    Q(promocode__products=None) | Q(promocode__products__in=[self.product])
                ) & Q(promocode__is_active=True) & (
                    Q(promocode__valid_from__isnull=True) | Q(promocode__valid_from__lte=today)
                ) & (
                    Q(promocode__valid_until__isnull=True) | Q(promocode__valid_until__gt=today)
                ),
                customer=customer,
                is_expired=False
            ).distinct()
            return all_codes

    def get_realprice(self):
        return self.unit_price


class ProductDocument(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
        related_name="product_document"
    )
    name = models.CharField(
        _("Document's Name"),
        max_length=50,
    )
    document = FilerFileField(
        verbose_name=_("Document"),
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = _("Product Document")
        verbose_name_plural = _("Product Documents")

    def __str__(self):
        return self.name


#######################################################################
# Plugins
#######################################################################


class dmSite(models.Model):
    """
    A model to replace sites.Site and help handles site's data.
    """

    site = models.ForeignKey(
        sites.models.Site,
        on_delete=models.CASCADE,
        related_name="dmsite"
    )
    google_analytics = models.TextField(
        verbose_name=_("Google Analytics Snippet"),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("Site")
        verbose_name_plural = _("Site")

    def __str__(self):
        return self.site.name


class dmSiteLogo(models.Model):
    """
    Logo's data (light and dark version) of the site.
    Can be used to easily retrieve and update logo
    all around the site.
    """

    site = models.ForeignKey(
        dmSite,
        on_delete=models.CASCADE,
        related_name="logos"
    )
    logolight = image.FilerImageField(
        verbose_name=_("Logo pour fond clair"),
        on_delete=models.SET_NULL,
        related_name="logo_light",
        blank=False,
        null=True
    )
    logodark = image.FilerImageField(
        verbose_name=_("Logo pour fond sombre"),
        on_delete=models.SET_NULL,
        related_name="logo_dark",
        blank=False,
        null=True
    )
    favico_180 = image.FilerImageField(
        verbose_name=_("Favicon 180x180"),
        on_delete=models.SET_NULL,
        related_name="favico_180",
        blank=True,
        null=True,
        help_text=_("Size: 180x180. Format: .png")
    )
    favico_192 = image.FilerImageField(
        verbose_name=_("Favicon 192x192"),
        on_delete=models.SET_NULL,
        related_name="favico_192",
        blank=True,
        null=True,
        help_text=_("Size: 192x192. Format: .png")
    )
    favico_512 = image.FilerImageField(
        verbose_name=_("Favicon 512x512"),
        on_delete=models.SET_NULL,
        related_name="favico_512",
        blank=True,
        null=True,
        help_text=_("Size: 512x512. Format: .png")
    )
    favico_ico = FilerFileField(
        verbose_name=_("Favicon 48x48"),
        on_delete=models.SET_NULL,
        related_name="favico_ico",
        blank=True,
        null=True,
        help_text=_("Size: 48x48. Format: .ico")
    )

    class Meta:
        verbose_name = _("Logo")
        verbose_name_plural = _("Logos")

    def __str__(self):
        return "Logo"


class dmSiteContact(models.Model):
    """
    Contact's data (phone, email, address, etc.) about the site.
    Can be used to easily retrieve and update contact's data
    all around the site.
    """

    site = models.ForeignKey(
        dmSite,
        on_delete=models.CASCADE,
        related_name="contacts"
    )
    phone = models.CharField(
        verbose_name=_("Phone"),
        max_length=20,
        blank=True,
        null=True
    )
    phone_secondary = models.CharField(
        verbose_name=_("Secondary Phone"),
        max_length=20,
        blank=True,
        null=True
    )
    email = models.CharField(
        verbose_name=_("Email"),
        max_length=1000,
        blank=True,
        null=True
    )
    address = models.CharField(
        verbose_name=_("Address"),
        max_length=1000,
        blank=True,
        null=True
    )
    schedule = models.TextField(
        verbose_name=_("Schedule"),
        blank=True,
        null=True
    )
    map_latitude = models.CharField(
        verbose_name=_("Map Latitude"),
        max_length=120,
        blank=True,
        null=True
    )
    map_longitude = models.CharField(
        verbose_name=_("Map Longitude"),
        max_length=120,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("Contacts")
        verbose_name_plural = _("Contacts")

    def __str__(self):
        return "Contacts"


class dmSiteSocial(models.Model):
    """
    Social media's links (facebook, intagram, youtube, etc.) of the site.
    Can be used to easily retrieve and update social medias
    all around the site.
    """

    CHOIX_SOCIALS = [
        (1, _("Facebook")),
        (2, _("Instagram")),
        (3, _("Youtube")),
        (4, _("Twitter"))
    ]

    site = models.ForeignKey(
        dmSite,
        on_delete=models.CASCADE,
        related_name="social"
    )
    social = models.PositiveSmallIntegerField(
        verbose_name=_("Social Network"),
        choices=CHOIX_SOCIALS,
        default=1
    )
    url = models.CharField(
        verbose_name=_("Link"),
        max_length=1000
    )

    class Meta:
        verbose_name = _("Social Network")
        verbose_name_plural = _("Social Networks")

    def __str__(self):
        return self.url


class dmSiteTermsAndConditions(TranslatableModel):
    """
    Terms and Conditions text of the site.
    Can be used to easily retrieve and show Terms and Conditions
    all around the site.
    """

    site = models.ForeignKey(
        dmSite,
        on_delete=models.CASCADE,
        related_name="termsandconditions"
    )
    text = TranslatedField()

    class Meta:
        verbose_name = _("Terms and Conditions")
        verbose_name_plural = _("Terms and Conditions")

    def __str__(self):
        return "Terms and Conditions"


class dmSiteTermsAndConditionsTranslation(TranslatedFieldsModel):
    """
    A model to handle translations of dmSiteTermsAndConditions
    """

    master = models.ForeignKey(
        dmSiteTermsAndConditions,
        on_delete=models.CASCADE,
        related_name="translations",
        null=True
    )
    text = HTMLField(
        verbose_name=_("Text"),
        configuration="CKEDITOR_SETTINGS_DESCRIPTION",
        blank=True,
        null=True
    )

    class Meta:
        unique_together = [("language_code", "master")]


#######################################################################
# Plugins
#######################################################################


class dmProductsCategories(CMSPlugin):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Maximum 100 characters.")
    )
    text = HTMLField(
        verbose_name=_("Text"),
        configuration="CKEDITOR_SETTINGS_DMPLUGIN",
        null=True,
        blank=True
    )
    label = models.CharField(
        verbose_name=_("Button's Label"),
        max_length=200,
        default="See all",
        null=True,
        blank=True,
        help_text=_("Leave blank to hide button.")
    )


class dmProductsVedette(CMSPlugin):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Maximum 100 characters.")
    )
    text = HTMLField(
        verbose_name=_("Text"),
        configuration="CKEDITOR_SETTINGS_DMPLUGIN",
        null=True,
        blank=True
    )


class dmProductsByCategory(CMSPlugin):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Maximum 100 characters.")
    )
    text = HTMLField(
        verbose_name=_("Text"),
        configuration="CKEDITOR_SETTINGS_DMPLUGIN",
        null=True,
        blank=True
    )
    text_color = ColorField(
        verbose_name=_("Text's Colour"),
        null=True,
        blank=True
    )
    bg_color = ColorField(
        verbose_name=_("Background's Colour"),
        null=True,
        blank=True
    )
    bg_image = image.FilerImageField(
        verbose_name=_("Background's Image"),
        on_delete=models.SET_NULL,
        related_name="bg_image",
        null=True,
        blank=True
    )


class dmProductsBrands(CMSPlugin):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Maximum 100 characters.")
    )
    text = HTMLField(
        verbose_name=_("Text"),
        configuration="CKEDITOR_SETTINGS_DMPLUGIN",
        null=True,
        blank=True
    )
    howmany = models.PositiveSmallIntegerField(
        verbose_name=_("Number"),
        default=5,
        blank=False,
        null=False,
        help_text=_("How many brand's logo to be show at the same time.")
    )


# ===---


class dmBlocEntete(CMSPlugin):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Maximum 255 characters.")
    )


class dmBlocTextMedia(CMSPlugin):
    CHOIX_POSITION = [
        (0, _("Left")),
        (1, _("Right"))
    ]
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Maximum 100 characters.")
    )
    subtitle = models.CharField(
        verbose_name=_("Subtitle"),
        max_length=200,
        null=True,
        blank=True,
        help_text=_("Maximum 200 characters.")
    )
    text = HTMLField(
        verbose_name=_("Text"),
        configuration="CKEDITOR_SETTINGS_DMBLOCKPLUGIN",
        null=True,
        blank=True
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        null=True,
        blank=True,
        help_text=_("Sizes : 398x531. Leave blank to hide image.")
    )
    video = FilerFileField(
        verbose_name=_("Video"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text=_("Leave blank to hide or use image instead.")
    )
    text_align = models.BooleanField(
        verbose_name=_("Align text and media vertically?"),
        default=True
    )
    colposition = models.PositiveSmallIntegerField(
        verbose_name=_("Image's Position"),
        choices=CHOIX_POSITION,
        default=1,
        null=False,
        blank=False
    )


class dmBlocTextCarrousel(CMSPlugin):
    CHOIX_POSITION = [
        (0, _("Left")),
        (1, _("Right"))
    ]
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Maximum 100 characters.")
    )
    subtitle = models.CharField(
        verbose_name=_("Subtitle"),
        max_length=200,
        null=True,
        blank=True,
        help_text=_("Maximum 200 characters.")
    )
    text = HTMLField(
        verbose_name=_("Text"),
        configuration="CKEDITOR_SETTINGS_DMBLOCKPLUGIN",
        null=True,
        blank=True
    )
    text_align = models.BooleanField(
        verbose_name=_("Align text and media vertically?"),
        default=True
    )
    colposition = models.PositiveSmallIntegerField(
        verbose_name=_("Image's Position"),
        choices=CHOIX_POSITION,
        default=1,
        null=False,
        blank=False
    )
    howmany_image = models.PositiveSmallIntegerField(
        verbose_name=_("How Many Images?"),
        default=1,
        help_text=_("How many images to show at the same time on desktop.")
    )
    crop_image = models.BooleanField(
        verbose_name=_("Crop Image?"),
        default=False,
        help_text=_("If checked, will crop images to fit the same ratio.")
    )
    see_dots = models.BooleanField(
        verbose_name=_("Show Dots?"),
        default=False,
        help_text=_("If checked, will display dots under carrousel for each image.")
    )
    see_navs = models.BooleanField(
        verbose_name=_("Show Navigation Arrows?"),
        default=True,
        help_text=_("If checked, will display navigation arrows both sides of the carrousel.")
    )


class dmBlocTextCarrouselImage(CMSPlugin):
    image = models.ImageField(
        verbose_name=_("Image"),
        null=False,
        blank=False,
        help_text=_("Max sizes : 600x600. Always use the same ratio on the same carrousel.")
    )


class dmBlocText2Column(CMSPlugin):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Maximum 100 characters.")
    )
    subtitle = models.CharField(
        verbose_name=_("Subtitle"),
        max_length=200,
        null=True,
        blank=True,
        help_text=_("Maximum 200 characters.")
    )
    text_left = HTMLField(
        verbose_name=_("Left Text"),
        configuration="CKEDITOR_SETTINGS_DMBLOCKPLUGIN",
        null=True,
        blank=True
    )
    text_right = HTMLField(
        verbose_name=_("Right Text"),
        configuration="CKEDITOR_SETTINGS_DMBLOCKPLUGIN",
        null=True,
        blank=True
    )
    text_align = models.BooleanField(
        verbose_name=_("Align texts vertically?"),
        default=False
    )


class dmBlocEnteteVideo(CMSPlugin):
    videofile = FilerFileField(
        verbose_name=_("Video File"),
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )


class dmBlocSliderParent(CMSPlugin):
    height = models.PositiveSmallIntegerField(
        verbose_name=_("Height"),
        default=500,
        help_text=_("Height of the slider (will be automatically shrinked on mobile version).")
    )


class dmBlocSliderChild(CMSPlugin):
    CHOICE_POS_TEXT = [
        (1, _("Left")),
        (2, _("Middle")),
        (3, _("Right"))
    ]
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Maximum 100 characters.")
    )
    suptitle = models.CharField(
        verbose_name=_("Suptitle"),
        max_length=200,
        null=True,
        blank=True,
        help_text=_("Maximum 200 characters.")
    )
    subtitle = models.CharField(
        verbose_name=_("Subtitle"),
        max_length=200,
        null=True,
        blank=True,
        help_text=_("Maximum 200 characters.")
    )
    title_color = ColorField(
        verbose_name=_("Title's Colour"),
        null=True,
        blank=True
    )
    suptitle_color = ColorField(
        verbose_name=_("Suptitle's Colour"),
        null=True,
        blank=True
    )
    subtitle_color = ColorField(
        verbose_name=_("Subtitle's Colour"),
        null=True,
        blank=True
    )
    position_text = models.PositiveSmallIntegerField(
        verbose_name=_("Text's Position"),
        choices=CHOICE_POS_TEXT,
        default=3
    )
    btn_label = models.CharField(
        verbose_name=_("Link's Label"),
        max_length=30,
        null=True,
        blank=True,
        help_text=_("Maximum 30 characters.")
    )
    btn_url = models.CharField(
        verbose_name=_("URL"),
        max_length=1000,
        blank=True,
        null=True,
        help_text=_("Maximum 1 000 characters.")
    )
    btn_blank = models.BooleanField(
        verbose_name=_("Open on new tab?"),
        default=False
    )
    bg_color = ColorField(
        verbose_name=_("Background's Colour"),
        null=True,
        blank=True
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        null=True,
        blank=True,
        help_text=_("Leave blank to hide image.")
    )


class dmBlocContact(CMSPlugin):
    horaire_top = models.CharField(
        verbose_name=_("Schedule - Top"),
        max_length=50,
        null=False,
        blank=False,
        help_text=_("Maximum 50 characters.")
    )
    horaire_bot = models.CharField(
        verbose_name=_("Schedule - Bottom"),
        max_length=50,
        null=False,
        blank=False,
        help_text=_("Maximum 50 characters.")
    )
    phone_top = models.CharField(
        verbose_name=_("Phone - Top"),
        max_length=50,
        null=False,
        blank=False,
        help_text=_("Maximum 50 characters.")
    )
    phone_bot = models.CharField(
        verbose_name=_("Phone - Bottom"),
        max_length=50,
        default="Call Us",
        null=False,
        blank=False,
        help_text=_("Maximum 50 characters.")
    )
    where_top = models.CharField(
        verbose_name=_("Address - Top"),
        max_length=120,
        null=False,
        blank=False,
        help_text=_("Maximum 120 characters.")
    )
    where_bot = models.CharField(
        verbose_name=_("Address - Bottom"),
        max_length=50,
        default="Our Address",
        null=False,
        blank=False,
        help_text=_("Maximum 50 characters.")
    )
    link_label = models.CharField(
        verbose_name=_("Button's Label"),
        max_length=50,
        default="Contact Us",
        null=False,
        blank=False,
        help_text=_("Maximum 50 characters.")
    )


class dmInfolettre(CMSPlugin):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Maximum 100 characters.")
    )
    title_color = ColorField(
        verbose_name=_("Title's Colour"),
        null=True,
        blank=True
    )
    subtitle = models.CharField(
        verbose_name=_("Subtitle"),
        max_length=200,
        null=True,
        blank=True,
        help_text=_("Maximum 200 characters.")
    )
    subtitle_color = ColorField(
        verbose_name=_("Subtitle's Colour"),
        null=True,
        blank=True
    )
    text = HTMLField(
        verbose_name=_("Text"),
        configuration="CKEDITOR_SETTINGS_DMPLUGIN",
        null=True,
        blank=True
    )
    text_color = ColorField(
        verbose_name=_("Text's Colour"),
        null=True,
        blank=True
    )
    label = models.CharField(
        verbose_name=_("Button's Label"),
        max_length=200,
        default="Subscribe to our newsletter",
        null=False,
        blank=False,
        help_text=_("Maximum 200 characters.")
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        null=True,
        blank=True,
        help_text=_("Leave blank to hide image.")
    )
    bg_color = ColorField(
        verbose_name=_("Background's Colour"),
        null=True,
        blank=True
    )


class dmBlocEtapesParent(CMSPlugin):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Maximum 100 characters.")
    )
    subtitle = models.CharField(
        verbose_name=_("Subtitle"),
        max_length=200,
        null=True,
        blank=True,
        help_text=_("Maximum 200 characters.")
    )


class dmBlocEtapesChild(CMSPlugin):
    image = models.ImageField(
        verbose_name=_("Image"),
        null=True,
        blank=True,
        help_text=_("Sizes : 160x160.")
    )
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
        null=True,
        blank=True
    )
    text = models.CharField(
        verbose_name=_("Text"),
        max_length=200,
        null=True,
        blank=True,
        help_text=_("Maximum 200 characters.")
    )


class dmBlockSalesParent(CMSPlugin):
    CHOIX_PERLINE = [
        (1, _("1 block")),
        (2, _("2 blocks")),
        (3, _("3 blocks"))
    ]
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Maximum 100 characters.")
    )
    text = HTMLField(
        verbose_name=_("Text"),
        configuration="CKEDITOR_SETTINGS_DMPLUGIN",
        null=True,
        blank=True
    )
    perline = models.PositiveSmallIntegerField(
        verbose_name=_("How many block per line?"),
        choices=CHOIX_PERLINE,
        default=2,
        null=False,
        blank=False
    )


class dmBlockSalesChild(CMSPlugin):
    CHOIX_POSITION = [
        (0, _("Left")),
        (1, _("Right"))
    ]
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Maximum 100 characters.")
    )
    text = models.CharField(
        verbose_name=_("Text"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Maximum 100 characters.")
    )
    txt_color = ColorField(
        verbose_name=_("Text's Colour"),
        default="#292b2c"
    )
    text_position = models.PositiveSmallIntegerField(
        verbose_name=_("Text's Position"),
        choices=CHOIX_POSITION,
        default=1,
        null=False,
        blank=False
    )
    btn_label = models.CharField(
        verbose_name=_("Button's Label"),
        max_length=25,
        null=True,
        blank=True,
        help_text=_("Maximum 25 characters.")
    )
    btn_url = models.CharField(
        verbose_name=_("Button's URL"),
        max_length=1000,
        null=True,
        blank=True
    )
    btn_text_color = ColorField(
        verbose_name=_("Button Text's Colour"),
        default="#292b2c"
    )
    btn_border_color = ColorField(
        verbose_name=_("Button Border's Colour"),
        null=True,
        blank=True,
        help_text=_("Leave blank to use transparent.")
    )
    btn_bg_color = ColorField(
        verbose_name=_("Button Background's Colour"),
        null=True,
        blank=True,
        help_text=_("Leave blank to use transparent.")
    )
    bg_color = ColorField(
        verbose_name=_("Background's Colour"),
        default="#f2f2f3"
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        null=True,
        blank=True
    )


class dmBlockCalltoaction(CMSPlugin):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=250,
        null=True,
        blank=True,
        help_text=_("Maximum 250 characters.")
    )
    subtitle = models.CharField(
        verbose_name=_("Subtitle"),
        max_length=250,
        null=True,
        blank=True,
        help_text=_("Maximum 250 characters.")
    )
    text = models.CharField(
        verbose_name=_("Text"),
        max_length=500,
        null=True,
        blank=True,
        help_text=_("Maximum 500 characters.")
    )
    title_color = ColorField(
        verbose_name=_("Title's Colour"),
        default="#292b2c"
    )
    subtitle_color = ColorField(
        verbose_name=_("Subtitle's Colour"),
        default="#292b2c"
    )
    text_color = ColorField(
        verbose_name=_("Text's Colour"),
        default="#292b2c"
    )
    btn_label = models.CharField(
        verbose_name=_("Button's Label"),
        max_length=25,
        null=True,
        blank=True,
        help_text=_("Maximum 25 characters.")
    )
    btn_url = models.CharField(
        verbose_name=_("Button's URL"),
        max_length=1000,
        null=True,
        blank=True
    )
    bg_color = ColorField(
        verbose_name=_("Background's Colour"),
        null=True,
        blank=True
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        null=True,
        blank=True
    )


class dmTeamParent(CMSPlugin):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Maximum 100 characters.")
    )
    text = HTMLField(
        verbose_name=_("Text"),
        configuration="CKEDITOR_SETTINGS_DMPLUGIN",
        null=True,
        blank=True
    )


class dmTeamChild(CMSPlugin):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=100,
        null=False,
        blank=False,
        help_text=_("Maximum 100 characters.")
    )
    job = models.CharField(
        verbose_name=_("Job"),
        max_length=1000,
        null=True,
        blank=True
    )
    photo = image.FilerImageField(
        verbose_name=_("Photo"),
        related_name="team_photo",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        max_length=250,
        null=True,
        blank=True
    )
    facebook = models.URLField(
        verbose_name="Facebook",
        max_length=250,
        null=True,
        blank=True,
        help_text=_("Ex.: https://www.facebook.com/<username>")
    )
    twitter = models.URLField(
        verbose_name="Twitter",
        max_length=250,
        null=True,
        blank=True,
        help_text=_("Ex.: https://twitter.com/<username>")
    )
    instagram = models.URLField(
        verbose_name="Instagram",
        max_length=250,
        null=True,
        blank=True,
        help_text=_("Ex.: https://www.instagram.com/<username>")
    )

class dmTestimonialParent(CMSPlugin):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Maximum 100 characters.")
    )
    text = HTMLField(
        verbose_name=_("Text"),
        configuration="CKEDITOR_SETTINGS_DMPLUGIN",
        null=True,
        blank=True
    )
    bg_color = ColorField(
        verbose_name=_("Background's Colour"),
        null=True,
        blank=True
    )
    bg_image = models.ImageField(
        verbose_name=_("Background's Image"),
        null=True,
        blank=True,
        help_text=_("Facultative. Size: 2000x900.")
    )

class dmTestimonialChild(CMSPlugin):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=250,
        null=True,
        blank=True,
        help_text=_("Maximum 250 characters.")
    )
    name_color = ColorField(
        verbose_name=_("Name's Colour"),
        default="#292b2c"
    )
    photo = models.ImageField(
        verbose_name=_("Photo"),
        null=True,
        blank=True
    )
    text = HTMLField(
        verbose_name=_("Text"),
        configuration="CKEDITOR_SETTINGS_DMPLUGIN",
        null=True,
        blank=True
    )


class FeatureList(models.Model):

    feature_name = models.CharField(
        verbose_name=_("Feature Name"),
        max_length=100
    )
    is_enabled = models.BooleanField(
        verbose_name=_("Is enabled?"),
        default=False
    )

    class Meta:
        verbose_name = _("Feature List")
        verbose_name_plural = _("Feature Lists")

    def __str__(self):
        return self.feature_name
