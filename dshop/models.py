import pytz
import re
from decimal import Decimal
from datetime import datetime
from cms.models import CMSPlugin
from colorfield.fields import ColorField
from polymorphic.query import PolymorphicQuerySet

from filer.fields import image
from filer.fields.file import FilerFileField

from parler.fields import TranslatedField
from parler.managers import TranslatableManager, TranslatableQuerySet
from parler.models import TranslatableModelMixin
from parler.models import TranslatedFieldsModel, TranslatedFields

from django.db import models
from django.db.models import Q
from django.contrib import sites
from django.core.validators import MinValueValidator
from djangocms_text_ckeditor.fields import HTMLField
from django.utils.six.moves.urllib.parse import urljoin
from django.utils.translation import ugettext_lazy as _
from autoslug import AutoSlugField

from shop.money import Money, MoneyMaker
from shop.money.fields import MoneyField
from shop.models.address import BaseShippingAddress, BaseBillingAddress
from shop.models.defaults.cart import Cart
from shop.models.defaults.cart_item import CartItem
from shop.models.defaults.customer import Customer
from shop.models.defaults.mapping import ProductPage, ProductImage
from shop.models.defaults.order import Order
from shop.models.fields import JSONField
from shop.models.order import BaseOrderItem
from shop.models.product import BaseProduct, BaseProductManager
from shop.models.product import AvailableProductMixin

try:
    from apps.dmRabais.models import dmRabaisPerCategory
    from apps.dmRabais.models import dmPromoCode
    from apps.dmRabais.models import dmCustomerPromoCode
except Exception:
    dmRabaisPerCategory = None
    dmPromoCode = None
    dmCustomerPromoCode = None

__all__ = ['Cart', 'CartItem', 'Order', 'Customer']

TAG_RE = re.compile(r'<[^>]+>')


class OrderItem(BaseOrderItem):
    quantity = models.PositiveIntegerField(_("Ordered quantity"))
    variables = JSONField(verbose_name=_("Données"))

    def populate_from_cart_item(self, cart_item, request):
        super().populate_from_cart_item(cart_item, request)
        self.variables = cart_item.extra
        self.save()


class CMSPageReferenceMixin(object):
    category_fields = ['cms_pages']

    def get_absolute_url(self):
        cms_page = self.cms_pages.order_by('node__path').last()
        if cms_page is None:
            return urljoin('/produit/', self.slug)
        return urljoin(cms_page.get_absolute_url(), self.slug)


class ProductQuerySet(TranslatableQuerySet, PolymorphicQuerySet):
    pass


class ProductManager(BaseProductManager, TranslatableManager):
    queryset_class = ProductQuerySet

    def get_queryset(self):
        qs = self.queryset_class(self.model, using=self._db)
        return qs.prefetch_related('translations')


#######################################################################
# Adresses
#######################################################################

COUNTRIES_FR = [('AF', _('Afghanistan')), ('ZA', _('Afrique du Sud')),
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
                ('NI', _('Nicaragua')), ('NE', _('Niger')), ('NG',
                                                             _('Nigeria')),
                ('NO', _('Norvège')), ('NZ', _('Nouvelle-Zélande')),
                ('OM', _('Oman')), ('UG', _('Ouganda')),
                ('UZ', _('Ouzbékistan')), ('PK', _('Pakistan')),
                ('PW', _('Palaos')), ('PA', _('Panama')),
                ('PG', _('Papouasie-Nouvelle-Guinée')), ('PY', _('Paraguay')),
                ('NL', _('Pays-Bas')), ('PE', _('Pérou')),
                ('PH', _('Philippines')), ('PL', _('Pologne')),
                ('PT', _('Portugal')), ('QA', _('Qatar')), ('RO',
                                                            _('Roumanie')),
                ('GB', _('Royaume-Uni')), ('RU', _('Russie')),
                ('RW', _('Rwanda')), ('KN', _('Saint-Christophe-et-Niévès')),
                ('SM', _('Saint-Marin')),
                ('VC', _('Saint-Vincent-et-les-Grenadines')),
                ('LC', _('Sainte-Lucie')), ('SB', _('Salomon')),
                ('WS', _('Samoa')), ('ST', _('Sao Tomé-et-Principe')),
                ('SN', _('Sénégal')), ('RS', _('Serbie')),
                ('SC', _('Seychelles')), ('SL', _('Sierra Leone')),
                ('SG', _('Singapour')), ('SK', _('Slovaquie')),
                ('SI', _('Slovénie')), ('SO', _('Somalie')), ('SD',
                                                              _('Soudan')),
                ('SS', _('Soudan du Sud')), ('LK', _('Sri Lanka')),
                ('SE', _('Suède')), ('CH', _('Suisse')), ('SR', _('Suriname')),
                ('SZ', _('Eswatini')), ('SY', _('Syrie')),
                ('TJ', _('Tadjikistan')), ('TZ', _('Tanzanie')),
                ('TD', _('Tchad')), ('CZ', _('Tchéquie')),
                ('TH', _('Thaïlande')), ('TL', _('Timor oriental')),
                ('TG', _('Togo')), ('TO', _('Tonga')),
                ('TT', _('Trinité-et-Tobago')), ('TN', _('Tunisie')),
                ('TM', _('Turkménistan')), ('TR', _('Turquie')),
                ('TV', _('Tuvalu')), ('UA', _('Ukraine')), ('UY',
                                                            _('Uruguay')),
                ('VU', _('Vanuatu')), ('VE', _('Venezuela')),
                ('VN', _('Viêt Nam')), ('YE', _('Yémen')), ('ZM', _('Zambie')),
                ('ZW', _('Zimbabwe'))]


class ShippingAddress(BaseShippingAddress):
    """
    Customer's shipping address.
    """

    name = models.CharField(_("Nom complet"), max_length=1024)
    address1 = models.CharField(_("Adresse 1"), max_length=1024)
    address2 = models.CharField(_("Adresse 2"),
                                max_length=1024,
                                blank=True,
                                null=True)
    country = models.CharField(_("Pays"), max_length=4)
    province = models.CharField(_("Province"), max_length=1024)
    city = models.CharField(_("Ville"), max_length=1024)
    zip_code = models.CharField(_("Code postal"), max_length=255)

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

    name = models.CharField(_("Nom complet"), max_length=1024)
    address1 = models.CharField(_("Adresse 1"), max_length=1024)
    address2 = models.CharField(_("Adresse 2"),
                                max_length=1024,
                                blank=True,
                                null=True)
    country = models.CharField(_("Pays"), max_length=4)
    province = models.CharField(_("Province"), max_length=1024)
    city = models.CharField(_("Ville"), max_length=1024)
    zip_code = models.CharField(_("Code postal"), max_length=255)

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


class ProductCategory(models.Model):
    """
    A model to help to categorize products.
    Product can have multiple categories.
    """

    name = models.CharField(verbose_name=_("Nom de la catégorie"),
                            max_length=100,
                            null=False,
                            blank=False)
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               verbose_name=_("Catégorie parente"),
                               blank=True,
                               null=True)
    order = models.PositiveSmallIntegerField(verbose_name=_("Ordre"),
                                             default=0,
                                             blank=False,
                                             null=False)

    class Meta:
        verbose_name = _("Catégorie de produit")
        verbose_name_plural = _("Catégories de produit")
        ordering = ["order", "parent__name", "name"]

    def __str__(self):
        if self.parent is not None:
            if self.parent.parent is not None:
                return self.parent.parent.name + ' | ' + self.parent.name + ' | ' + self.name
            else:
                return self.parent.name + ' | ' + self.name
        else:
            return self.name

    def get_products(self):
        result = ProductDefault.objects.filter(
            Q(categories=self) | Q(categories__parent=self)
            | Q(categories__parent__parent=self)
            | Q(categories__parent__parent__parent=self),
            active=True).order_by('id')
        return result


class ProductFilter(models.Model):
    """
    A model to help to filter products.
    Product can have multiple filters.
    """

    name = models.CharField(verbose_name=_("Nom du filtre"),
                            max_length=100,
                            null=False,
                            blank=False)
    order = models.PositiveSmallIntegerField(verbose_name=_("Ordre"),
                                             default=0,
                                             blank=False,
                                             null=False)

    class Meta:
        verbose_name = _("Filtre de produit")
        verbose_name_plural = _("Filtres de produit")
        ordering = ["order", "name"]

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
        _("Nom du produit"),
        max_length=255
    )
    slug = AutoSlugField(populate_from='product_name',
                         unique=True
    )
    categories = models.ManyToManyField(
        ProductCategory,
        verbose_name=_("Catégories"),
        blank=True
    )
    filters = models.ManyToManyField(
        ProductFilter,
        verbose_name=_("Filtres"),
        blank=True
    )
    is_vedette = models.BooleanField(
        _("En vedette ?"),
        default=False
    )
    caption = TranslatedField()
    description = TranslatedField()
    order = models.PositiveIntegerField(_("Sort by"), db_index=True)
    cms_pages = models.ManyToManyField('cms.Page', through=ProductPage)
    main_image = image.FilerImageField(verbose_name=_("Image principale"),
                                       on_delete=models.SET_NULL,
                                       related_name="main_image",
                                       null=True,
                                       blank=True)
    images = models.ManyToManyField('filer.Image', through=ProductImage)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['order']

    objects = ProductManager()

    lookup_fields = ['product_name__icontains', 'description__icontains']

    def __str__(self):
        return self.product_name

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

    master = models.ForeignKey(Product,
                               on_delete=models.CASCADE,
                               related_name='translations',
                               null=True)
    caption = HTMLField(verbose_name=_("Caption"),
                        configuration='CKEDITOR_SETTINGS_CAPTION',
                        blank=True,
                        null=True,
                        help_text=_("Description courte."))
    description = HTMLField(
        verbose_name=_("Description"),
        configuration='CKEDITOR_SETTINGS_DESCRIPTION',
        blank=True,
        null=True,
        help_text=_("Description longue."),
    )

    class Meta:
        unique_together = [('language_code', 'master')]


# ===---


class ProductDefault(AvailableProductMixin, Product):
    """
    A basic Product, polymorphic child of Product
    """

    product_code = models.CharField(_("Code du produit"),
                                    max_length=255,
                                    unique=True,
                                    help_text=_("Un code unique."))
    unit_price = MoneyField(_("Unit price"),
                            decimal_places=3,
                            help_text=_("Net price for this product"))
    quantity = models.PositiveIntegerField(
        _("Quantity"),
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_("Available quantity in stock"))
    multilingual = TranslatedFields(
        description=HTMLField(verbose_name=_("Description"),
                              configuration='CKEDITOR_SETTINGS_DESCRIPTION',
                              help_text=_("Description longue.")))

    class Meta:
        verbose_name = _("Produit par défaut")
        verbose_name_plural = _("Produits par défaut")

    @property
    def get_caption(self):
        if self.caption:
            c = TAG_RE.sub('', self.caption)
            return c
        return ''

    @property
    def get_description(self):
        if self.description:
            desc = TAG_RE.sub('', self.description)
            return desc
        return ''

    def get_price(self, request):
        r = self.unit_price
        if request:
            # ===--- GET DISCOUNTS
            if dmRabaisPerCategory is not None:
                today = pytz.utc.localize(datetime.utcnow())
                all_discounts = dmRabaisPerCategory.objects.filter(
                    Q(categories__in=self.categories.all()) & Q(is_active=True)
                    & (Q(valid_from__isnull=True) | Q(valid_from__lte=today))
                    & (Q(valid_until__isnull=True) | Q(valid_until__gt=today)))
                if all_discounts.count() > 0:
                    for d in all_discounts:
                        if d.amount is not None:
                            r = Money(Decimal(r) - Decimal(d.amount))
                        elif d.percent is not None:
                            pourcent = Decimal(d.percent) / Decimal('100')
                            discount = Money(
                                Decimal(self.unit_price) * pourcent)
                            r = r - discount
            # ===--- GET PROMOCODE
            if dmPromoCode is not None:
                if request.user.is_authenticated:
                    today = pytz.utc.localize(datetime.utcnow())
                    all_codes = dmCustomerPromoCode.objects.filter(
                        (Q(promocode__categories=None)
                         | Q(promocode__categories__in=self.categories.all()))
                        & (Q(promocode__products=None)
                           | Q(promocode__products__in=[self]))
                        & Q(promocode__is_active=True) &
                        (Q(promocode__valid_from__isnull=True)
                         | Q(promocode__valid_from__lte=today)) &
                        (Q(promocode__valid_until__isnull=True)
                         | Q(promocode__valid_until__gt=today)),
                        customer=request.user.customer,
                        is_expired=False)
                    if all_codes.count() > 0:
                        for d in all_codes:
                            if d.promocode.amount is not None:
                                r = Money(
                                    Decimal(r) - Decimal(d.promocode.amount))
                            elif d.promocode.percent is not None:
                                pourcent = Decimal(
                                    d.promocode.percent) / Decimal('100')
                                discount = Money(
                                    Decimal(self.unit_price) * pourcent)
                                r = r - discount
        if Decimal(r) <= 0:
            r = Money(0)
        return r

    def get_promocodes(self, request):
        if dmPromoCode is not None:
            if request.user.is_authenticated:
                today = pytz.utc.localize(datetime.utcnow())
                all_codes = dmCustomerPromoCode.objects.filter(
                    (Q(promocode__categories=None)
                     | Q(promocode__categories__in=self.categories.all())) &
                    (Q(promocode__products=None)
                     | Q(promocode__products__in=[self]))
                    & Q(promocode__is_active=True) &
                    (Q(promocode__valid_from__isnull=True)
                     | Q(promocode__valid_from__lte=today)) &
                    (Q(promocode__valid_until__isnull=True)
                     | Q(promocode__valid_until__gt=today)),
                    customer=request.user.customer,
                    is_expired=False)
                return all_codes

    def get_realprice(self):
        return self.unit_price


# ===---


class ProductVariable(Product):
    """
    A basic variable Product, polymorphic child of Product,
    parent of ProductVariableVariant.
    """

    multilingual = TranslatedFields(
        description=HTMLField(verbose_name=_("Description"),
                              configuration='CKEDITOR_SETTINGS_DESCRIPTION',
                              help_text=_("Description longue.")))

    class Meta:
        verbose_name = _("Produit variable")
        verbose_name_plural = _("Produits variables")

    default_manager = ProductManager()

    @property
    def get_caption(self):
        if self.caption:
            c = TAG_RE.sub('', self.caption)
            return c
        return ''

    @property
    def get_description(self):
        if self.description:
            desc = TAG_RE.sub('', self.description)
            return desc
        return ''

    def get_price(self, request):
        if not hasattr(self, '_price'):
            if self.variants.exists():
                currency = self.variants.first().unit_price.currency
                aggr = self.variants.aggregate(models.Min('unit_price'))
                self._price = MoneyMaker(currency)(aggr['unit_price__min'])
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
            product_code = kwargs['product_code']
        except KeyError:
            return
        cart_item_qs = CartItem.objects.filter(cart=cart, product=self)
        for cart_item in cart_item_qs:
            if cart_item.product_code == product_code:
                return cart_item

    def get_product_variant(self, **kwargs):
        try:
            product_code = kwargs.get('product_code')
            return self.variants.get(product_code=product_code)
        except ProductVariableVariant.DoesNotExist as e:
            raise ProductVariable.DoesNotExist(e)

    def get_product_variants(self):
        return self.variants.all()


class ProductVariableVariant(AvailableProductMixin, models.Model):
    """
    A basic variant of ProductVariable, will be used to populate
    cart item data.
    """

    product = models.ForeignKey(ProductVariable,
                                on_delete=models.CASCADE,
                                verbose_name=_("Produit"),
                                related_name='variants')
    product_code = models.CharField(_("Product code"),
                                    max_length=255,
                                    unique=True)
    unit_price = MoneyField(_("Unit price"),
                            decimal_places=3,
                            help_text=_("Net price for this product"))
    quantity = models.PositiveIntegerField(
        _("Quantity"),
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_("Available quantity in stock"))

    def __str__(self):
        return _("{product}").format(product=self.product)

    def get_price(self, request):
        r = self.unit_price
        if request:
            # ===--- GET DISCOUNTS
            if dmRabaisPerCategory is not None:
                today = pytz.utc.localize(datetime.utcnow())
                all_discounts = dmRabaisPerCategory.objects.filter(
                    Q(categories__in=self.product.categories.all())
                    & Q(is_active=True)
                    & (Q(valid_from__isnull=True) | Q(valid_from__lte=today))
                    & (Q(valid_until__isnull=True) | Q(valid_until__gt=today)))
                if all_discounts.count() > 0:
                    for d in all_discounts:
                        if d.amount is not None:
                            r = Money(Decimal(r) - Decimal(d.amount))
                        elif d.percent is not None:
                            pourcent = Decimal(d.percent) / Decimal("100")
                            discount = Money(
                                Decimal(self.unit_price) * pourcent)
                            r = r - discount
            # ===--- GET PROMOCODE
            if dmPromoCode is not None:
                if request.user.is_authenticated:
                    today = pytz.utc.localize(datetime.utcnow())
                    all_codes = dmCustomerPromoCode.objects.filter(
                        (Q(promocode__categories=None)
                         | Q(promocode__categories__in=self.product.categories.
                             all())) &
                        (Q(promocode__products=None)
                         | Q(promocode__products__in=[self.product]))
                        & Q(promocode__is_active=True) &
                        (Q(promocode__valid_from__isnull=True)
                         | Q(promocode__valid_from__lte=today)) &
                        (Q(promocode__valid_until__isnull=True)
                         | Q(promocode__valid_until__gt=today)),
                        customer=request.user.customer,
                        is_expired=False)
                    if all_codes.count() > 0:
                        for d in all_codes:
                            if d.promocode.amount is not None:
                                r = Money(
                                    Decimal(r) - Decimal(d.promocode.amount))
                            elif d.promocode.percent is not None:
                                pourcent = Decimal(
                                    d.promocode.percent) / Decimal('100')
                                discount = Money(
                                    Decimal(self.unit_price) * pourcent)
                                r = r - discount
        if Decimal(r) <= 0:
            r = Money(0)
        return r

    def get_promocodes(self, request):
        if dmPromoCode is not None:
            if request.user.is_authenticated:
                today = pytz.utc.localize(datetime.utcnow())
                all_codes = dmCustomerPromoCode.objects.filter(
                    (Q(promocode__categories=None) |
                     Q(promocode__categories__in=self.product.categories.all())
                     ) & (Q(promocode__products=None)
                          | Q(promocode__products__in=[self.product]))
                    & Q(promocode__is_active=True) &
                    (Q(promocode__valid_from__isnull=True)
                     | Q(promocode__valid_from__lte=today)) &
                    (Q(promocode__valid_until__isnull=True)
                     | Q(promocode__valid_until__gt=today)),
                    customer=request.user.customer,
                    is_expired=False)
                return all_codes

    def get_realprice(self):
        return self.unit_price


#######################################################################
# Plugins
#######################################################################


class dmSite(models.Model):
    """
    A model to replace sites.Site and help handles site's data.
    """

    site = models.ForeignKey(sites.models.Site, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Site")
        verbose_name_plural = _("Site")

    def __str__(self):
        return self.site.name


class dmSiteContact(models.Model):
    """
    Contact's data (phone, email, address, etc.) about the site.
    Can be used to easily retrieve and update contact's data
    all around the site.
    """

    site = models.ForeignKey(dmSite,
                             on_delete=models.CASCADE,
                             related_name="contacts")
    phone = models.CharField(verbose_name=_("Téléphone"),
                             max_length=25,
                             blank=True,
                             null=True)
    email = models.CharField(verbose_name=_("Courriel"),
                             max_length=1000,
                             blank=True,
                             null=True)
    address = models.CharField(verbose_name=_("Adresse"),
                               max_length=1000,
                               blank=True,
                               null=True)

    class Meta:
        verbose_name = _("Contacts")
        verbose_name_plural = _("Contacts")

    def __str__(self):
        return 'Contacts'


class dmSiteSocial(models.Model):
    """
    Social media's links (facebook, intagram, youtube, etc.) of the site.
    Can be used to easily retrieve and update social medias
    all around the site.
    """

    CHOIX_SOCIALS = [(1, "Facebook"), (2, "Instagram"), (3, "Youtube")]

    site = models.ForeignKey(dmSite,
                             on_delete=models.CASCADE,
                             related_name="social")
    social = models.PositiveSmallIntegerField(verbose_name=_("Réseau social"),
                                              choices=CHOIX_SOCIALS,
                                              default=1)
    url = models.CharField(verbose_name=_("Lien vers le réseau"),
                           max_length=1000)

    class Meta:
        verbose_name = _("Réseau social")
        verbose_name_plural = _("Réseaux sociaux")

    def __str__(self):
        return self.url


#######################################################################
# Plugins
#######################################################################


class dmProductsCategories(CMSPlugin):
    title = models.CharField(verbose_name=_("Titre"),
                             max_length=100,
                             null=True,
                             blank=True)
    text = HTMLField(verbose_name=_("Texte"),
                     configuration='CKEDITOR_SETTINGS_DMPLUGIN',
                     null=True,
                     blank=True)
    label = models.CharField(
        verbose_name=_("Texte du bouton"),
        max_length=200,
        default="Voir tout",
        null=True,
        blank=True,
        help_text=
        "Laisser vide pour ne pas afficher le bouton vers les produits.")


class dmProductsVedette(CMSPlugin):
    title = models.CharField(verbose_name=_("Titre"),
                             max_length=100,
                             null=True,
                             blank=True)
    text = HTMLField(verbose_name=_("Texte"),
                     configuration='CKEDITOR_SETTINGS_DMPLUGIN',
                     null=True,
                     blank=True)


class dmProductsByCategory(CMSPlugin):
    title = models.CharField(verbose_name=_("Titre"),
                             max_length=100,
                             null=True,
                             blank=True)
    text = HTMLField(verbose_name=_("Texte"),
                     configuration='CKEDITOR_SETTINGS_DMPLUGIN',
                     null=True,
                     blank=True)


# ===---


class dmBlocEntete(CMSPlugin):
    title = models.CharField(verbose_name=_("Titre"),
                             max_length=255,
                             null=True,
                             blank=True)


class dmBlocTextMedia(CMSPlugin):
    CHOIX_POSITION = [(0, _("Gauche")), (1, _("Droite"))]
    title = models.CharField(verbose_name=_("Titre"),
                             max_length=100,
                             null=True,
                             blank=True)
    subtitle = models.CharField(verbose_name=_("Sous-titre"),
                                max_length=200,
                                null=True,
                                blank=True)
    text = HTMLField(verbose_name=_("Texte"),
                     configuration='CKEDITOR_SETTINGS_DMBLOCKPLUGIN',
                     null=True,
                     blank=True)
    image = models.ImageField(
        verbose_name=_("Image"),
        null=True,
        blank=True,
        help_text=_(
            "Dimension : 398x531. Laisser vide pour ne pas afficher d'image."))
    colposition = models.PositiveSmallIntegerField(
        verbose_name=_("Position de l'image"),
        choices=CHOIX_POSITION,
        default=1,
        null=False,
        blank=False)


class dmBlocEnteteVideo(CMSPlugin):
    videofile = FilerFileField(verbose_name=_("Fichier vidéo"),
                               on_delete=models.CASCADE,
                               null=False,
                               blank=False)


class dmBlocSliderParent(CMSPlugin):
    pass


class dmBlocSliderChild(CMSPlugin):
    CHOICE_POS_TEXT = [(1, _('Gauche')), (2, _('Centre')), (3, _('Droite'))]
    title = models.CharField(verbose_name=_("Titre"),
                             max_length=100,
                             null=True,
                             blank=True)
    subtitle = models.CharField(verbose_name=_("Sous-titre"),
                                max_length=200,
                                null=True,
                                blank=True)
    title_color = ColorField(verbose_name=_("Couleur du titre"),
                             null=True,
                             blank=True)
    subtitle_color = ColorField(verbose_name=_("Couleur du sous-titre"),
                                null=True,
                                blank=True)
    position_text = models.PositiveSmallIntegerField(
        verbose_name=_("Position du texte"),
        choices=CHOICE_POS_TEXT,
        default=3)
    btn_label = models.CharField(verbose_name=_("Nom du lien"),
                                 max_length=30,
                                 null=True,
                                 blank=True)
    btn_url = models.CharField(verbose_name=_("Adresse URL du lien"),
                               max_length=1000,
                               blank=True,
                               null=True)
    btn_blank = models.BooleanField(
        verbose_name=_("Le lien s'ouvre dans un nouvel onglet ?"),
        default=False)
    bg_color = ColorField(verbose_name=_("Couleur de fond"),
                          null=True,
                          blank=True)
    image = models.ImageField(
        verbose_name=_("Image"),
        null=True,
        blank=True,
        help_text=_("Laisser vide pour ne pas afficher d'image."))


class dmBlocContact(CMSPlugin):
    horaire_top = models.CharField(verbose_name=_("Horaire - Haut"),
                                   max_length=50,
                                   null=False,
                                   blank=False)
    horaire_bot = models.CharField(verbose_name=_("Horaire - Bas"),
                                   max_length=50,
                                   null=False,
                                   blank=False)
    phone_top = models.CharField(verbose_name=_("Téléphone - Haut"),
                                 max_length=50,
                                 null=False,
                                 blank=False)
    phone_bot = models.CharField(verbose_name=_("Téléphone - Bas"),
                                 max_length=50,
                                 default="Appelez-nous",
                                 null=False,
                                 blank=False)
    where_top = models.CharField(verbose_name=_("Adresse - Haut"),
                                 max_length=120,
                                 null=False,
                                 blank=False)
    where_bot = models.CharField(verbose_name=_("Adresse - Bas"),
                                 max_length=50,
                                 default="Notre adresse",
                                 null=False,
                                 blank=False)
    link_label = models.CharField(verbose_name=_("Texte du bouton"),
                                  max_length=50,
                                  default="Contacter Nancy",
                                  null=False,
                                  blank=False)


class dmInfolettre(CMSPlugin):
    title = models.CharField(verbose_name=_("Titre"),
                             max_length=100,
                             null=True,
                             blank=True)
    subtitle = models.CharField(verbose_name=_("Sous-titre"),
                                max_length=200,
                                null=True,
                                blank=True)
    text = HTMLField(verbose_name=_("Texte"),
                     configuration='CKEDITOR_SETTINGS_DMPLUGIN',
                     null=True,
                     blank=True)
    label = models.CharField(verbose_name=_("Texte du bouton"),
                             max_length=200,
                             default="S'inscrire à l'infolettre",
                             null=False,
                             blank=False)
    image = models.ImageField(verbose_name=_("Image"), null=True, blank=True)


class dmBlocEtapesParent(CMSPlugin):
    title = models.CharField(verbose_name=_("Titre"),
                             max_length=100,
                             null=True,
                             blank=True)
    subtitle = models.CharField(verbose_name=_("Sous-titre"),
                                max_length=200,
                                null=True,
                                blank=True)


class dmBlocEtapesChild(CMSPlugin):
    image = models.ImageField(verbose_name=_("Image"),
                              null=True,
                              blank=True,
                              help_text=_("Dimension : 160x160."))
    title = models.CharField(verbose_name=_("Titre"),
                             max_length=100,
                             null=True,
                             blank=True)
    text = models.CharField(verbose_name=_("Texte"),
                            max_length=200,
                            null=True,
                            blank=True)


class dmBlockSalesParent(CMSPlugin):
    title = models.CharField(verbose_name=_("Titre"),
                             max_length=100,
                             null=True,
                             blank=True)
    text = HTMLField(verbose_name=_("Texte"),
                     configuration='CKEDITOR_SETTINGS_DMPLUGIN',
                     null=True,
                     blank=True)


class dmBlockSalesChild(CMSPlugin):
    title = models.CharField(verbose_name=_("Titre"),
                             max_length=100,
                             null=True,
                             blank=True)
    text = models.CharField(verbose_name=_("Texte"),
                            max_length=100,
                            null=True,
                            blank=True)
    txt_color = ColorField(verbose_name=_("Couleur du texte"),
                           default="#292b2c")
    btn_label = models.CharField(verbose_name=_("Button's Label"),
                                 max_length=25,
                                 null=True,
                                 blank=True)
    btn_url = models.CharField(verbose_name=_("Button's URL"),
                               max_length=255,
                               null=True,
                               blank=True)
    bg_color = ColorField(verbose_name=_("Couleur de fond"), default="#f2f2f3")
    image = models.ImageField(verbose_name="Image", null=True, blank=True)


class dmBlockCalltoaction(CMSPlugin):
    title = models.CharField(verbose_name=_("Titre"),
                             max_length=100,
                             null=True,
                             blank=True)
    subtitle = models.CharField(verbose_name=_("Sous-titre"),
                                max_length=100,
                                null=True,
                                blank=True)
    text = models.CharField(verbose_name=_("Texte"),
                            max_length=100,
                            null=True,
                            blank=True)
    title_color = ColorField(verbose_name=_("Couleur du titre"),
                             default="#292b2c")
    subtitle_color = ColorField(verbose_name=_("Couleur du sous-titre"),
                                default="#292b2c")
    text_color = ColorField(verbose_name=_("Couleur du texte"),
                            default="#292b2c")
    btn_label = models.CharField(verbose_name=_("Button's Label"),
                                 max_length=25,
                                 null=True,
                                 blank=True)
    btn_url = models.CharField(verbose_name=_("Button's URL"),
                               max_length=255,
                               null=True,
                               blank=True)
    bg_color = ColorField(verbose_name=_("Couleur de fond"),
                          null=True,
                          blank=True)
    image = models.ImageField(verbose_name="Image", null=True, blank=True)


class FeatureList(models.Model):

    feature_name = models.CharField(verbose_name=_('Feature Name'),
                                    max_length=100)
    is_enabled = models.BooleanField(verbose_name=_('Is FeatureEemable?'),
                                     default=False)

