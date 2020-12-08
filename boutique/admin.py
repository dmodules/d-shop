from django.contrib import admin
from django.template.context import Context
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from parler.admin import TranslatableAdmin
from filer.models import ThumbnailOption
from cms.admin.placeholderadmin import PlaceholderAdminMixin, FrontendEditableAdminMixin
from shop.admin.defaults import customer
from shop.models.defaults.order import Order
from shop.models.cart import CartModel, CartItemModel
from shop.admin.order import BaseOrderAdmin, PrintInvoiceAdminMixin
from adminsortable2.admin import SortableAdminMixin, PolymorphicSortableAdminMixin
from shop.admin.product import CMSPageAsCategoryMixin, UnitPriceMixin, ProductImageInline, InvalidateProductCacheMixin, SearchProductIndexMixin, CMSPageFilter
from polymorphic.admin import (PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter)
from shop.money import Money
from decimal import Decimal

from shop.admin.order import OrderItemInline

from boutique.models import dmSite, dmSiteContact, dmSiteSocial
from boutique.models import dmAlertPublicitaire
from boutique.models import dmRabaisPerCategory
from boutique.models import CanadaTaxManagement, ShippingManagement, StripeOrderData
from boutique.models import BillingAddress, ShippingAddress
from boutique.models import ProductCategory, ProductFilter
from boutique.models import Product
from boutique.models import ProductDefault
from boutique.models import ProductVariable, ProductVariableVariant

admin.site.site_header = "Administration"
admin.site.unregister(ThumbnailOption)

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

__all__ = ['customer']

#######################################################################
# Site
#######################################################################

class dmSiteContactInline(admin.TabularInline):
  model = dmSiteContact
  extra = 1
  max_num = 1

class dmSiteSocialInline(admin.TabularInline):
  model = dmSiteSocial
  extra = 1

@admin.register(dmSite)
class dmSiteAdmin(admin.ModelAdmin):
  list_display = ['get_name', 'site']
  inlines = [dmSiteContactInline, dmSiteSocialInline]

  def get_name(self, obj):
    return obj.site.name
  get_name.short_description = _("Nom")

#######################################################################
# Billing and Shipping
#######################################################################

@admin.register(CanadaTaxManagement)
class CanadaTaxManagementAdmin(admin.ModelAdmin):
  list_display = ['state', 'hst', 'gst', 'pst', 'qst']

@admin.register(ShippingManagement)
class ShippingManagementAdmin(admin.ModelAdmin):
  list_display = ['name', 'get_price', 'identifier']

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
  pass

@admin.register(BillingAddress)
class BillingAddressAdmin(admin.ModelAdmin):
  pass

#######################################################################
# Panier
#######################################################################

class CartItemModelInline(admin.TabularInline):
  model = CartItemModel
  extra = 0

#@admin.register(CartModel)
class BaseCartAdmin(admin.ModelAdmin):
  list_display = ['pk','customer']
  inlines = [CartItemModelInline]

#######################################################################
# Commande
#######################################################################

class dmOrderItemInline(OrderItemInline):
  fields = [
    ('product_code', 'unit_price', 'line_total',),
    ('quantity',),
    'get_variables',
    #'extra',
    #'render_as_html_extra',
  ]
  readonly_fields = ['product_code', 'quantity', 'unit_price', 'line_total', 'get_variables']

  def get_variables(self, obj):
    dd = obj.variables["variables"]
    r = ""
    for k, v in dd.items():
      r = r + k.upper() + " : " + v + "\n"
    return r
  get_variables.short_description = _("Données")

@admin.register(Order)
class OrderAdmin(PrintInvoiceAdminMixin, BaseOrderAdmin):
  list_filter = []
  fields = [
    'get_ordernumber',
    'get_customer_link',
    'get_status',
    'get_date',
    #'updated_at',
    'get_subtotal',
    'get_total',
    'is_fully_paid',
    'render_as_html_extra'
  ]
  readonly_fields = ['get_ordernumber', 'get_status', 'get_date', 'get_total', 'get_subtotal', 'get_customer_link', 'get_outstanding_amount', 'updated_at', 'render_as_html_extra', 'stored_request', 'is_fully_paid']
  inlines = [dmOrderItemInline]

  class Meta:
    verbose_name = _("Commande")
    verbose_name_plural = _("Commandes")

  def get_queryset(self, request):
    print(self)
    return super(OrderAdmin, self).get_queryset(request).filter(status="payment_confirmed")

  def get_ordernumber(self, obj):
    return obj.get_number()
  get_ordernumber.short_description = _("Numéro")

  def get_status(self, obj):
    return obj._transition_targets.get(obj.status, obj.status)
  get_status.short_description = _("Status")

  def get_date(self, obj):
    return obj.created_at.strftime("%d-%m-%Y, %H:%M:%S")
  get_date.short_description = _("Créée le")

  def get_subtotal(self, obj):
    return str(obj.subtotal)
  get_subtotal.short_description = _("Sous-total")

  def get_total(self, obj):
    return str(obj.total)
  get_total.short_description = _("Total")

  def is_fully_paid(self, obj):
    return obj.is_fully_paid()
  is_fully_paid.short_description = _("Is fully paid")
  is_fully_paid.boolean = True

  def render_as_html_extra(self, obj):
    return self.extra_template.render(obj.extra)
  render_as_html_extra.short_description = _("Détails")

  def has_delete_permission(self, request, obj=None):
    return False

#######################################################################
# Produit: Catégorie
#######################################################################

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
  list_display = ['name', 'parent', 'order']
  list_filter = ['parent']

@admin.register(ProductFilter)
class ProductFilterAdmin(admin.ModelAdmin):
  list_display = ['name', 'order']

#######################################################################
# Rabais
#######################################################################

@admin.register(dmRabaisPerCategory)
class dmRabaisPerCategoryAdmin(admin.ModelAdmin):
  verbose_name = _("Rabais")
  verbose_name_plural = _("Rabais")
  fieldsets = [
    (None, {
      'fields': [
          'name',
          'amount',
          'percent',
          'is_active',
          ('valid_from', 'valid_until'),
          'categories',
      ]
    })
  ]
  list_display = ['name', "get_discount", "is_active", "get_debut", "get_fin"]
  list_filter = ['is_active', "categories"]
  filter_horizontal = ['categories']
  search_fields = ['name']

  def get_discount(self, obj):
    if obj.amount is not None:
      return Money(obj.amount)
    elif obj.percent is not None:
      return str(Decimal(obj.percent)) + "%"
    else:
      return "-"
  get_discount.short_description = _("Rabais")

  def get_debut(self, obj):
    return obj.valid_from
  get_debut.short_description = _("Début")

  def get_fin(self, obj):
    return obj.valid_until
  get_fin.short_description = _("Fin")

#######################################################################
# Produits
#######################################################################

@admin.register(ProductDefault)
class ProductDefaultAdmin(InvalidateProductCacheMixin, SortableAdminMixin, TranslatableAdmin, FrontendEditableAdminMixin, PlaceholderAdminMixin, PolymorphicChildModelAdmin):
  base_model = Product
  fieldsets = (
    (None, {
      'fields': [
        ('product_name', 'slug'),
        ('product_code', 'unit_price'),
          'quantity',
          'active',
          'is_vedette',
      ],
    }),
    (_("Translatable Fields"), {
      'fields': ['caption', 'description'],
    }),
    (_("Catégories"), {
      'fields': ["categories"],
    }),
    (_("Image Principale"), {
      'fields': [
        'main_image'
      ]
    })
  )
  inlines = [ProductImageInline]
  filter_horizontal = ["categories"]
  prepopulated_fields = {'slug': ['product_code']}

class ProductVariableVariantInline(admin.TabularInline):
    model = ProductVariableVariant
    extra = 0

@admin.register(ProductVariable)
class ProductVariableAdmin(InvalidateProductCacheMixin, SortableAdminMixin, TranslatableAdmin, FrontendEditableAdminMixin, PlaceholderAdminMixin, PolymorphicChildModelAdmin):
  base_model = Product
  fieldsets = [
    (None, {
      'fields': [
        ('product_name', 'slug'),
        'active',
        'is_vedette',
      ],
    }),
    (_("Translatable Fields"), {
        'fields': ['caption', 'description'],
    }),
    (_("Catégories"), {
      'fields': ["categories"],
    }),
    (_("Image Principale"), {
      'fields': [
        'main_image'
      ]
    })
  ]
  filter_horizontal = ["categories"]
  inlines = [ProductImageInline, ProductVariableVariantInline]
  prepopulated_fields = {'slug': ['product_name']}

  def render_text_index(self, instance):
    template = get_template('search/indexes/boutique/commodity_text.txt')
    return template.render(Context({'object': instance}))
  render_text_index.short_description = _("Text Index")

@admin.register(Product)
class ProductAdmin(PolymorphicSortableAdminMixin, PolymorphicParentModelAdmin):
  base_model = Product
  child_models = [ProductDefault, ProductVariable]
  list_display = ['product_name', 'get_price', 'product_type', "get_quantity", 'is_vedette', 'active']
  list_display_links = ['product_name']
  search_fields = ['product_name']
  list_filter = [PolymorphicChildModelFilter, CMSPageFilter]
  list_per_page = 250
  list_max_show_all = 1000

  def get_price(self, obj):
    return str(obj.get_real_instance().get_price(None))
  get_price.short_description = _("Price starting at")

  def get_quantity(self, obj):
    result = obj.get_real_instance()
    try:
      d = []
      for v in result.variants.all():
        d.append(str(v.quantity))
      result = ', '.join(d)
    except:
      result = result.quantity
    return str(result)
  get_quantity.short_description = _("Quantity")

#######################################################################
# Alerte Publicitaire
#######################################################################

@admin.register(dmAlertPublicitaire)
class dmAlertPublicitaireAdmin(admin.ModelAdmin):
  list_display = ["text", "link", "get_debut", "get_fin", "is_active"]
  list_filter = ["is_active"]
  search_fields = ["text", "link"]

  def get_debut(self, obj):
    return obj.valid_from
  get_debut.short_description = _("Début")

  def get_fin(self, obj):
    return obj.valid_until
  get_fin.short_description = _("Fin")

#######################################################################
# Stripe
#######################################################################

@admin.register(StripeOrderData)
class StripeOrderDataAdmin(admin.ModelAdmin):
  list_display = ['order_payment', 'receipt_url', ]


