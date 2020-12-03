from cms import __version__ as CMS_VERSION
from django.utils.translation import ugettext_lazy as _
import pytz
from cms.models import CMSPlugin
from filer.fields import image
from filer.fields.file import FilerFileField
from shop.models.fields import JSONField
from colorfield.fields import ColorField
from datetime import datetime
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.fields import HTMLField
from polymorphic.query import PolymorphicQuerySet
from parler.managers import TranslatableManager, TranslatableQuerySet
from parler.models import TranslatableModelMixin, TranslatedFieldsModel, TranslatedFields
from parler.fields import TranslatedField
from cms.models.fields import PlaceholderField
from shop.money import Money, MoneyMaker
from shop.money.fields import MoneyField
from shop.models.product import BaseProduct, BaseProductManager, AvailableProductMixin
from shop.models.defaults.cart import Cart
from shop.models.defaults.cart_item import CartItem
from shop.models.order import BaseOrderItem
from shop.models.defaults.order import Order
from shop.models.defaults.mapping import ProductPage, ProductImage
from shop.models.address import BaseShippingAddress, BaseBillingAddress
from shop.models.defaults.customer import Customer
from django.db.models import Q
from distutils.version import LooseVersion
from django.utils.six.moves.urllib.parse import urljoin
from .stripe_tax import create_tax, update_tax
from shop.models.order import OrderPayment

__all__ = ['Cart', 'CartItem', 'Order', 'Customer']

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
    if LooseVersion(CMS_VERSION) < LooseVersion('3.5'):
      cms_page = self.cms_pages.order_by('depth').last()
    else:
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

COUNTRIES_FR = [
  ('AF', _('Afghanistan')),
  ('ZA', _('Afrique du Sud')),
  ('AL', _('Albanie')),
  ('DZ', _('Algérie')),
  ('DE', _('Allemagne')),
  ('AD', _('Andorre')),
  ('AO', _('Angola')),
  ('AG', _('Antigua-et-Barbuda')),
  ('SA', _('Arabie saoudite')),
  ('AR', _('Argentine')),
  ('AM', _('Arménie')),
  ('AU', _('Australie')),
  ('AT', _('Autriche')),
  ('AZ', _('Azerbaïdjan')),
  ('BS', _('Bahamas')),
  ('BH', _('Bahreïn')),
  ('BD', _('Bangladesh')),
  ('BB', _('Barbade')),
  ('BY', _('Biélorussie')),
  ('BE', _('Belgique')),
  ('BZ', _('Belize')),
  ('BJ', _('Bénin')),
  ('BT', _('Bhoutan')),
  ('BO', _('Bolivie')),
  ('BA', _('Bosnie-Herzégovine')),
  ('BW', _('Botswana')),
  ('BR', _('Brésil')),
  ('BN', _('Brunei')),
  ('BG', _('Bulgarie')),
  ('BF', _('Burkina Faso')),
  ('BI', _('Burundi')),
  ('KH', _('Cambodge')),
  ('CM', _('Cameroun')),
  ('CA', _('Canada')),
  ('CV', _('Cap-Vert')),
  ('CF', _('République centrafricaine')),
  ('CL', _('Chili')),
  ('CN', _('Chine')),
  ('CY', _('Chypre (pays)')),
  ('CO', _('Colombie')),
  ('KM', _('Comores (pays)')),
  ('CG', _('République du Congo')),
  ('CD', _('République démocratique du Congo')),
  ('KR', _('Corée du Sud')),
  ('KP', _('Corée du Nord')),
  ('CR', _('Costa Rica')),
  ('CI', _("Côte d'Ivoire")),
  ('HR', _('Croatie')),
  ('CU', _('Cuba')),
  ('DK', _('Danemark')),
  ('DJ', _('Djibouti')),
  ('DO', _('République dominicaine')),
  ('DM', _('Dominique')),
  ('EG', _('Égypte')),
  ('SV', _('Salvador')),
  ('AE', _('Émirats arabes unis')),
  ('EC', _('Équateur (pays)')),
  ('ER', _('Érythrée')),
  ('ES', _('Espagne')),
  ('EE', _('Estonie')),
  ('US', _('États-Unis')),
  ('ET', _('Éthiopie')),
  ('FJ', _('Fidji')),
  ('FI', _('Finlande')),
  ('FR', _('France')),
  ('GA', _('Gabon')),
  ('GM', _('Gambie')),
  ('GE', _('Géorgie (pays)')),
  ('GH', _('Ghana')),
  ('GR', _('Grèce')),
  ('GD', _('Grenade (pays)')),
  ('GT', _('Guatemala')),
  ('GN', _('Guinée')),
  ('GW', _('Guinée-Bissau')),
  ('GQ', _('Guinée équatoriale')),
  ('GY', _('Guyana')),
  ('HT', _('Haïti')),
  ('HN', _('Honduras')),
  ('HU', _('Hongrie')),
  ('IN', _('Inde')),
  ('ID', _('Indonésie')),
  ('IR', _('Iran')),
  ('IQ', _('Irak')),
  ('IE', _('Irlande (pays)')),
  ('IS', _('Islande')),
  ('IL', _('Israël')),
  ('IT', _('Italie')),
  ('JM', _('Jamaïque')),
  ('JP', _('Japon')),
  ('JO', _('Jordanie')),
  ('KZ', _('Kazakhstan')),
  ('KE', _('Kenya')),
  ('KG', _('Kirghizistan')),
  ('KI', _('Kiribati')),
  ('KW', _('Koweït')),
  ('LA', _('Laos')),
  ('LS', _('Lesotho')),
  ('LV', _('Lettonie')),
  ('LB', _('Liban')),
  ('LR', _('Liberia')),
  ('LY', _('Libye')),
  ('LI', _('Liechtenstein')),
  ('LT', _('Lituanie')),
  ('LU', _('Luxembourg (pays)')),
  ('MK', _('Macédoine du Nord')),
  ('MG', _('Madagascar')),
  ('MY', _('Malaisie')),
  ('MW', _('Malawi')),
  ('MV', _('Maldives')),
  ('ML', _('Mali')),
  ('MT', _('Malte')),
  ('MA', _('Maroc')),
  ('MH', _('Îles Marshall (pays)')),
  ('MU', _('Maurice (pays)')),
  ('MR', _('Mauritanie')),
  ('MX', _('Mexique')),
  ('FM', _('États fédérés de Micronésie (pays)')),
  ('MD', _('Moldavie')),
  ('MC', _('Monaco')),
  ('MN', _('Mongolie')),
  ('ME', _('Monténégro')),
  ('MZ', _('Mozambique')),
  ('MM', _('Birmanie')),
  ('NA', _('Namibie')),
  ('NR', _('Nauru')),
  ('NP', _('Népal')),
  ('NI', _('Nicaragua')),
  ('NE', _('Niger')),
  ('NG', _('Nigeria')),
  ('NO', _('Norvège')),
  ('NZ', _('Nouvelle-Zélande')),
  ('OM', _('Oman')),
  ('UG', _('Ouganda')),
  ('UZ', _('Ouzbékistan')),
  ('PK', _('Pakistan')),
  ('PW', _('Palaos')),
  ('PA', _('Panama')),
  ('PG', _('Papouasie-Nouvelle-Guinée')),
  ('PY', _('Paraguay')),
  ('NL', _('Pays-Bas')),
  ('PE', _('Pérou')),
  ('PH', _('Philippines')),
  ('PL', _('Pologne')),
  ('PT', _('Portugal')),
  ('QA', _('Qatar')),
  ('RO', _('Roumanie')),
  ('GB', _('Royaume-Uni')),
  ('RU', _('Russie')),
  ('RW', _('Rwanda')),
  ('KN', _('Saint-Christophe-et-Niévès')),
  ('SM', _('Saint-Marin')),
  ('VC', _('Saint-Vincent-et-les-Grenadines')),
  ('LC', _('Sainte-Lucie')),
  ('SB', _('Salomon')),
  ('WS', _('Samoa')),
  ('ST', _('Sao Tomé-et-Principe')),
  ('SN', _('Sénégal')),
  ('RS', _('Serbie')),
  ('SC', _('Seychelles')),
  ('SL', _('Sierra Leone')),
  ('SG', _('Singapour')),
  ('SK', _('Slovaquie')),
  ('SI', _('Slovénie')),
  ('SO', _('Somalie')),
  ('SD', _('Soudan')),
  ('SS', _('Soudan du Sud')),
  ('LK', _('Sri Lanka')),
  ('SE', _('Suède')),
  ('CH', _('Suisse')),
  ('SR', _('Suriname')),
  ('SZ', _('Eswatini')),
  ('SY', _('Syrie')),
  ('TJ', _('Tadjikistan')),
  ('TZ', _('Tanzanie')),
  ('TD', _('Tchad')),
  ('CZ', _('Tchéquie')),
  ('TH', _('Thaïlande')),
  ('TL', _('Timor oriental')),
  ('TG', _('Togo')),
  ('TO', _('Tonga')),
  ('TT', _('Trinité-et-Tobago')),
  ('TN', _('Tunisie')),
  ('TM', _('Turkménistan')),
  ('TR', _('Turquie')),
  ('TV', _('Tuvalu')),
  ('UA', _('Ukraine')),
  ('UY', _('Uruguay')),
  ('VU', _('Vanuatu')),
  ('VE', _('Venezuela')),
  ('VN', _('Viêt Nam')),
  ('YE', _('Yémen')),
  ('ZM', _('Zambie')),
  ('ZW', _('Zimbabwe'))
]

class ShippingAddress(BaseShippingAddress):
  name = models.CharField(_("Nom complet"), max_length=1024)
  address1 = models.CharField(_("Adresse 1"), max_length=1024)
  address2 = models.CharField(_("Adresse 2"), max_length=1024, blank=True, null=True)
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
  name = models.CharField(_("Nom complet"), max_length=1024)
  address1 = models.CharField(_("Adresse 1"), max_length=1024)
  address2 = models.CharField(_("Adresse 2"), max_length=1024, blank=True, null=True)
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
  name = models.CharField(verbose_name=_("Nom de la catégorie"), max_length=100, null=False, blank=False)
  parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name=_("Catégorie parente"), blank=True, null=True)
  order = models.PositiveSmallIntegerField(verbose_name=_("Ordre"), default=0, blank=False, null=False)

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
    result = ProductDefault.objects.filter(Q(categories=self)|Q(categories__parent=self)|Q(categories__parent__parent=self)|Q(categories__parent__parent__parent=self), active=True).order_by('id')
    return result

class ProductFilter(models.Model):
  name = models.CharField(verbose_name=_("Nom du filtre"), max_length=100, null=False, blank=False)
  order = models.PositiveSmallIntegerField(verbose_name=_("Ordre"), default=0, blank=False, null=False)

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
  product_name = models.CharField(_("Nom du produit"), max_length=255)
  slug = models.SlugField(_("Slug"), unique=True)
  categories = models.ManyToManyField(ProductCategory, verbose_name=_("Catégories"))
  filters = models.ManyToManyField(ProductFilter, verbose_name=_("Filtres"))
  is_vedette = models.BooleanField(_("En vedette ?"), default=False)
  caption = TranslatedField()
  description = TranslatedField()
  order = models.PositiveIntegerField(_("Sort by"), db_index=True)
  cms_pages = models.ManyToManyField('cms.Page', through=ProductPage)
  main_image = image.FilerImageField(verbose_name=_("Image principale"), on_delete=models.CASCADE, related_name="main_image", null=True, blank=True)
  images = models.ManyToManyField('filer.Image', through=ProductImage)

  class Meta:
    verbose_name = _("Product")
    verbose_name_plural = _("Products")
    ordering = ['order']

  objects = ProductManager()

  lookup_fields = ['product_name__icontains']

  def __str__(self):
    return self.product_name

  @property
  def sample_image(self):
    if self.main_image:
      return self.main_image
    else:
      return self.images.first()

class ProductTranslation(TranslatedFieldsModel):
  master = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='translations', null=True)
  caption = HTMLField(verbose_name=_("Caption"), blank=True, null=True, configuration='CKEDITOR_SETTINGS_CAPTION', help_text=_("Description courte."))
  description = HTMLField(verbose_name=_("Description"), configuration='CKEDITOR_SETTINGS_DESCRIPTION', help_text=_("Description longue."), blank=True, null=True)

  class Meta:
    unique_together = [('language_code', 'master')]

# ===---

class ProductDefault(AvailableProductMixin, Product):
  product_code = models.CharField(_("Code du produit"),max_length=255, unique=True, help_text=_("Un code unique."))
  unit_price = MoneyField(_("Unit price"), decimal_places=3, help_text=_("Net price for this product"))
  quantity = models.PositiveIntegerField(_("Quantity"), default=0, validators=[MinValueValidator(0)], help_text=_("Available quantity in stock"))
  multilingual = TranslatedFields(description=HTMLField(verbose_name=_("Description"), configuration='CKEDITOR_SETTINGS_DESCRIPTION', help_text=_("Description longue.")))

  class Meta:
    verbose_name = _("Produit par défaut")
    verbose_name_plural = _("Produits par défaut")

  def get_price(self, request):
    today = pytz.utc.localize(datetime.utcnow())
    all_discounts = dmRabaisPerCategory.objects.filter(Q(categories__in=self.categories.all()) & Q(is_active=True) & (Q(valid_from__isnull=True) | Q(valid_from__lte=today)) & (Q(valid_until__isnull=True) | Q(valid_until__gt=today)))
    if all_discounts.count() > 0:
      r = self.unit_price
      for d in all_discounts:
        if d.amount is not None:
          r = Money(Decimal(r) - Decimal(d.amount))
        elif d.percent is not None:
          pourcent = Decimal(d.percent) / Decimal('100')
          discount = Money(Decimal(self.unit_price) * pourcent)
          r = r - discount
    else:
      r = self.unit_price
    if Decimal(r) < 0:
      r = Money(0)
    return r

  def get_realprice(self):
    return self.unit_price

# ===---

class ProductVariable(Product):
  multilingual = TranslatedFields(description=HTMLField(verbose_name=_("Description"), configuration='CKEDITOR_SETTINGS_DESCRIPTION', help_text=_("Description longue.")))

  class Meta:
    verbose_name = _("Produit variable")
    verbose_name_plural = _("Produits variables")

  default_manager = ProductManager()

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
  product = models.ForeignKey(ProductVariable, on_delete=models.CASCADE, verbose_name=_("Produit"), related_name='variants')
  product_code = models.CharField(_("Product code"),max_length=255, unique=True)
  unit_price = MoneyField(_("Unit price"), decimal_places=3, help_text=_("Net price for this product"))
  quantity = models.PositiveIntegerField(_("Quantity"), default=0, validators=[MinValueValidator(0)], help_text=_("Available quantity in stock"))

  def __str__(self):
    return _("{product}").format(product=self.product)

  def get_price(self, request):
    today = pytz.utc.localize(datetime.utcnow())
    all_discounts = dmRabaisPerCategory.objects.filter(Q(categories__in=self.product.categories.all()) & Q(is_active=True) & (Q(valid_from__isnull=True) | Q(valid_from__lte=today)) & (Q(valid_until__isnull=True) | Q(valid_until__gt=today)))
    if all_discounts.count() > 0:
      r = self.unit_price
      for d in all_discounts:
        if d.amount is not None:
          r = Money(Decimal(r) - Decimal(d.amount))
        elif d.percent is not None:
          pourcent = Decimal(d.percent) / Decimal('100')
          discount = Money(Decimal(self.unit_price) * pourcent)
          r = r - discount
    else:
      r = self.unit_price
    if Decimal(r) < 0:
      r = Money(0)
    return r

  def get_realprice(self):
    return self.unit_price

#######################################################################
# Rabais
#######################################################################

class dmRabaisPerCategory(models.Model):
  name = models.CharField(_('Nom'), max_length=100)
  amount = models.DecimalField(verbose_name=_("Montant fixe"), max_digits=30, decimal_places=3, blank=True, null=True, help_text=_("Un montant fixe à retirer du prix original, laisser vide pour privilégier le pourcentage."))
  percent = models.PositiveSmallIntegerField(verbose_name=_("Pourcentage"), blank=True, null=True, help_text=_("Un pourcentage à retirer du prix original, ne sera pas utilisé s'il y a un montant dans 'Montant fixe'."))
  is_active = models.BooleanField(_('Actif'), default=True)
  valid_from = models.DateTimeField(_('Date de début'), default=datetime.now)
  valid_until = models.DateTimeField(_('Date de fin'), blank=True, null=True)
  categories = models.ManyToManyField(ProductCategory, related_name="rabaispercategory", verbose_name=_("Categories"))

  class Meta:
    verbose_name = _('Rabais par catégorie')
    verbose_name_plural = _('Rabais par catégorie')

  def __str__(self):
    return self.name

#######################################################################
# Alerte Publicitaire
#######################################################################

class dmAlertPublicitaire(models.Model):
  text = models.CharField(verbose_name=_("Texte"), max_length=75, help_text=_("Maximum de 75 caractères."))
  link = models.CharField(verbose_name=_("Lien URL"), max_length=1000, blank=True, null=True, help_text=_("Exemple: https://www.test.com. Laissez vide pour ne pas utiliser de lien."))
  open_blank = models.BooleanField(verbose_name=_("Ouvrir le lien dans un nouvel onglet ?"), default=False)
  is_active = models.BooleanField(_('Actif'), default=True)
  valid_from = models.DateTimeField(_('Date de début'), default=datetime.now)
  valid_until = models.DateTimeField(_('Date de fin'), blank=True, null=True)

  class Meta:
    verbose_name = _('Alerte publicitaire')
    verbose_name_plural = _('Alertes publicitaires')

  def __str__(self):
    return self.text

#######################################################################
# Plugins
#######################################################################

class dmProductsCategories(CMSPlugin):
  title = models.CharField(verbose_name=_("Titre"), max_length=100, null=True, blank=True)
  text = HTMLField(verbose_name=_("Texte"), configuration='CKEDITOR_SETTINGS_DMPLUGIN', null=True, blank=True)
  label = models.CharField(verbose_name=_("Texte du bouton"), max_length=200, default="Voir tout", null=True, blank=True, help_text="Laisser vide pour ne pas afficher le bouton vers les produits.")

class dmProductsVedette(CMSPlugin):
  title = models.CharField(verbose_name=_("Titre"), max_length=100, null=True, blank=True)
  text = HTMLField(verbose_name=_("Texte"), configuration='CKEDITOR_SETTINGS_DMPLUGIN', null=True, blank=True)

class dmProductsByCategory(CMSPlugin):
  title = models.CharField(verbose_name=_("Titre"), max_length=100, null=True, blank=True)
  text = HTMLField(verbose_name=_("Texte"), configuration='CKEDITOR_SETTINGS_DMPLUGIN', null=True, blank=True)

# ===---

class dmBlocEntete(CMSPlugin):
  title = models.CharField(verbose_name=_("Titre"), max_length=255, null=True, blank=True)

class dmBlocTextMedia(CMSPlugin):
  CHOIX_POSITION = [
    (0, _("Gauche")),
    (1, _("Droite"))
  ]
  title = models.CharField(verbose_name=_("Titre"), max_length=100, null=True, blank=True)
  subtitle = models.CharField(verbose_name=_("Sous-titre"), max_length=200, null=True, blank=True)
  text = HTMLField(verbose_name=_("Texte"), configuration='CKEDITOR_SETTINGS_DMBLOCKPLUGIN', null=True, blank=True)
  image = models.ImageField(verbose_name=_("Image"), null=True, blank=True, help_text=_("Dimension : 398x531. Laisser vide pour ne pas afficher d'image."))
  colposition = models.PositiveSmallIntegerField(verbose_name=_("Position de l'image"), choices=CHOIX_POSITION, default=1, null=False, blank=False)

class dmBlocEnteteVideo(CMSPlugin):
  videofile = FilerFileField(verbose_name=_("Fichier vidéo"), on_delete=models.CASCADE, null=False, blank=False)

class dmBlocSliderParent(CMSPlugin):
  pass

class dmBlocSliderChild(CMSPlugin):
  CHOICE_POS_TEXT = [
    (1, _('Gauche')),
    (2, _('Centre')),
    (3, _('Droite'))
  ]
  title = models.CharField(verbose_name=_("Titre"), max_length=100, null=True, blank=True)
  subtitle = models.CharField(verbose_name=_("Sous-titre"), max_length=200, null=True, blank=True)
  title_color = ColorField(verbose_name=_("Couleur du titre"), null=True, blank=True)
  subtitle_color = ColorField(verbose_name=_("Couleur du sous-titre"), null=True, blank=True)
  position_text = models.PositiveSmallIntegerField(verbose_name=_("Position du texte"), choices=CHOICE_POS_TEXT, default=3)
  btn_label = models.CharField(verbose_name=_("Nom du lien"), max_length=30, null=True, blank=True)
  btn_url = models.CharField(verbose_name=_("Adresse URL du lien"), max_length=1000, blank=True, null=True)
  btn_blank = models.BooleanField(verbose_name=_("Le lien s'ouvre dans un nouvel onglet ?"), default=False)
  bg_color = ColorField(verbose_name=_("Couleur de fond"), null=True, blank=True)
  image = models.ImageField(verbose_name=_("Image"), null=True, blank=True, help_text=_("Laisser vide pour ne pas afficher d'image."))

class dmBlocContact(CMSPlugin):
  horaire_top = models.CharField(verbose_name=_("Horaire - Haut"), max_length=50, null=False, blank=False)
  horaire_bot = models.CharField(verbose_name=_("Horaire - Bas"), max_length=50, null=False, blank=False)
  phone_top = models.CharField(verbose_name=_("Téléphone - Haut"), max_length=50, null=False, blank=False)
  phone_bot = models.CharField(verbose_name=_("Téléphone - Bas"), max_length=50, default="Appelez-nous", null=False, blank=False)
  where_top = models.CharField(verbose_name=_("Adresse - Haut"), max_length=120, null=False, blank=False)
  where_bot = models.CharField(verbose_name=_("Adresse - Bas"), max_length=50, default="Notre adresse", null=False, blank=False)
  link_label = models.CharField(verbose_name=_("Texte du bouton"), max_length=50, default="Contacter Nancy", null=False, blank=False)

class dmInfolettre(CMSPlugin):
  title = models.CharField(verbose_name=_("Titre"), max_length=100, null=True, blank=True)
  subtitle = models.CharField(verbose_name=_("Sous-titre"), max_length=200, null=True, blank=True)
  text = HTMLField(verbose_name=_("Texte"), configuration='CKEDITOR_SETTINGS_DMPLUGIN', null=True, blank=True)
  label = models.CharField(verbose_name=_("Texte du bouton"), max_length=200, default="S'inscrire à l'infolettre", null=False, blank=False)
  image = models.ImageField(verbose_name=_("Image"), null=True, blank=True)

class dmBlocEtapesParent(CMSPlugin):
  title = models.CharField(verbose_name=_("Titre"), max_length=100, null=True, blank=True)
  subtitle = models.CharField(verbose_name=_("Sous-titre"), max_length=200, null=True, blank=True)

class dmBlocEtapesChild(CMSPlugin):
  image = models.ImageField(verbose_name=_("Image"), null=True, blank=True, help_text=_("Dimension : 160x160."))
  title = models.CharField(verbose_name=_("Titre"), max_length=100, null=True, blank=True)
  text = models.CharField(verbose_name=_("Texte"), max_length=200, null=True, blank=True)

class dmBlockSalesParent(CMSPlugin):
  title = models.CharField(verbose_name=_("Titre"), max_length=100, null=True, blank=True)
  text = HTMLField(verbose_name=_("Texte"), configuration='CKEDITOR_SETTINGS_DMPLUGIN', null=True, blank=True)

class dmBlockSalesChild(CMSPlugin):
  title = models.CharField(verbose_name=_("Titre"), max_length=100, null=True, blank=True)
  text = models.CharField(verbose_name=_("Texte"), max_length=100, null=True, blank=True)
  btn_label = models.CharField(verbose_name=_("Button's Label"), max_length=25, null=True, blank=True)
  btn_url = models.CharField(verbose_name=_("Button's URL"), max_length=255, null=True, blank=True)
  image = models.ImageField(verbose_name="Image", null=True, blank=True)

#######################################################################
# Canada Taxes
#######################################################################

class CanadaTaxManagement(models.Model):
    state = models.CharField(
        _("Province"),
        choices=[2 * ('{}'.format(t),)
                 for t in ['Alberta', 'British Columbia', 'Manitoba',
                           'New-Brunswick', 'Newfoundland and Labrador',
                           'Northwest Territories', 'Nova Scotia', 'Nunavut',
                           'Ontario', 'Prince Edward Island', 'Quebec',
                           'Saskatchewan', 'Yukon']],
        max_length=60,
        unique=True,

    )
    hst = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        null=True, blank=True)
    gst = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        null=True, blank=True)
    pst = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        null=True, blank=True)
    qst = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        null=True, blank=True)

    stripe_hst = models.CharField(max_length=50, null=True, blank=True)
    stripe_gst = models.CharField(max_length=50, null=True, blank=True)
    stripe_pst = models.CharField(max_length=50, null=True, blank=True)
    stripe_qst = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = _("Taxe canadienne")
        verbose_name_plural = _("Taxes canadiennes")

    def __str__(self):
        return self.state

    def save(self, *args, **kwargs):

        if self._state.adding:
            hst, gst, pst, qst = create_tax(self)
            self.stripe_hst = hst
            self.stripe_gst = gst
            self.stripe_pst = pst
            self.stripe_qst = qst
        #else:
        #    update_tax(self)
        super(CanadaTaxManagement, self).save(*args, **kwargs)

class ShippingManagement(models.Model):
  CHOICE_IDENTIFIER = [
    ('free-shipping', _('Envoi postal (gratuit)')),
    ('standard-shipping', _('Envoi postal (standard)')),
    ('express-shipping', _('Envoi postal (express)')),
  ]
  name = models.CharField(verbose_name=_("Nom de la méthode d'expédition"), max_length=255, blank=False, null=False)
  identifier = models.CharField(verbose_name=_("Identifiant"), max_length=100, choices=CHOICE_IDENTIFIER, default='free-shipping', unique=True, blank=False, null=False)
  price = models.DecimalField(_("Prix"), max_digits=30, decimal_places=3, help_text=_("Un prix fixe ajouté au prix total du panier."))

  class Meta:
    verbose_name = _("Méthode d'expédition")
    verbose_name_plural = _("Méthodes d'expédition")

  def get_price(self):
      return str(self.price)

  get_price.short_description = _("Prix")

#######################################################################
# Stripe
#######################################################################

class StripeOrderData(models.Model):
  order_payment = models.OneToOneField(OrderPayment, on_delete=models.CASCADE, primary_key=True,)
  receipt_url = models.CharField(verbose_name=_("URL de réception"), max_length=150)
  stripe_session_data = models.TextField(verbose_name=_("Stripe données"))
  stripe_payment_data = models.TextField(verbose_name=_("Stripe de la facture"))

  def __str__(self):
    return str(self.order_payment)
