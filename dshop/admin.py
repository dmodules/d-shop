import pytz

from datetime import datetime, timedelta

from django.contrib import admin
from django.template.context import Context
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _

from cms.admin.placeholderadmin import PlaceholderAdminMixin
from cms.admin.placeholderadmin import FrontendEditableAdminMixin

from adminsortable2.admin import SortableAdminMixin
from adminsortable2.admin import PolymorphicSortableAdminMixin

from polymorphic.admin import (
    PolymorphicParentModelAdmin,
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter
)

from parler.admin import TranslatableAdmin

from filer.models import ThumbnailOption

from shop.admin.defaults import customer
from shop.admin.product import ProductImageInline
from shop.admin.product import InvalidateProductCacheMixin
from shop.admin.product import CMSPageFilter
from shop.admin.order import BaseOrderAdmin, PrintInvoiceAdminMixin
from shop.admin.order import OrderItemInline
from shop.models.defaults.order import Order
from shop.models.cart import CartItemModel

from dshop.models import dmSite, dmSiteLogo, dmSiteContact, dmSiteSocial
from dshop.models import BillingAddress, ShippingAddress
from dshop.models import ProductCategory, ProductFilter, ProductBrand
from dshop.models import Product
from dshop.models import ProductDefault
from dshop.models import ProductVariable, ProductVariableVariant
from dshop.models import FeatureList
from shop.admin.delivery import DeliveryOrderAdminMixin

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

__all__ = ["customer"]

#######################################################################
# Site
#######################################################################

class dmSiteLogoInline(admin.TabularInline):
    model = dmSiteLogo
    extra = 1
    max_num = 1


class dmSiteContactInline(admin.TabularInline):
    model = dmSiteContact
    extra = 1
    max_num = 1


class dmSiteSocialInline(admin.TabularInline):
    model = dmSiteSocial
    extra = 1


@admin.register(dmSite)
class dmSiteAdmin(admin.ModelAdmin):
    list_display = ["get_name", "site"]
    inlines = [
        dmSiteLogoInline,
        dmSiteContactInline,
        dmSiteSocialInline
    ]

    def get_name(self, obj):
        return obj.site.name
    get_name.short_description = _("Name")

#######################################################################
# Billing and Shipping
#######################################################################


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

# @admin.register(CartModel)


class BaseCartAdmin(admin.ModelAdmin):
    list_display = ["pk", "customer"]
    inlines = [CartItemModelInline]

#######################################################################
# Commande
#######################################################################


class dmOrderItemInline(OrderItemInline):
    fields = [
        ("product_code", "unit_price", "line_total"),
        ("quantity",),
        "get_variables",
        # 'extra',
        # 'render_as_html_extra',
    ]
    readonly_fields = [
        "product_code",
        "quantity",
        "unit_price",
        "line_total",
        "get_variables"
    ]

    def get_variables(self, obj):
        dd = obj.variables["variables"]
        r = ""
        for k, v in dd.items():
            r = r + k.upper() + " : " + v + "\n"
        return r
    get_variables.short_description = _("Data")


@admin.register(Order)
class OrderAdmin(DeliveryOrderAdminMixin, PrintInvoiceAdminMixin, BaseOrderAdmin):
    list_filter = []
    fields = [
        "get_ordernumber",
        "get_customer_link",
        "get_status",
        "get_date",
        # "updated_at",
        "get_subtotal",
        "get_total",
        "is_fully_paid",
        "render_as_html_extra"
    ]
    readonly_fields = [
        "get_ordernumber",
        "get_status",
        "get_date",
        "get_total",
        "get_subtotal",
        "get_customer_link",
        "get_outstanding_amount",
        "updated_at",
        "render_as_html_extra",
        "stored_request",
        "is_fully_paid"
    ]
    inlines = [dmOrderItemInline]

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def get_queryset(self, request):
        rr = super(OrderAdmin, self).get_queryset(request)
        for r in rr:
            today = pytz.utc.localize(datetime.utcnow())
            if r.status == "new" and r.updated_at + timedelta(hours=1) < today:
                r.delete()
            if r.status == "created" and r.updated_at + timedelta(hours=6) < today:
                r.delete()
        return super(OrderAdmin, self).get_queryset(request).all()

    def get_ordernumber(self, obj):
        return obj.get_number()
    get_ordernumber.short_description = _("Number")

    def get_status(self, obj):
        return obj._transition_targets.get(obj.status, obj.status)
    get_status.short_description = _("Status")

    def get_date(self, obj):
        return obj.created_at.strftime("%d-%m-%Y, %H:%M:%S")
    get_date.short_description = _("Created at")

    def get_subtotal(self, obj):
        return str(obj.subtotal)
    get_subtotal.short_description = _("Subtotal")

    def get_total(self, obj):
        return str(obj.total)
    get_total.short_description = _("Total")

    def is_fully_paid(self, obj):
        return obj.is_fully_paid()
    is_fully_paid.short_description = _("Is fully paid")
    is_fully_paid.boolean = True

    def render_as_html_extra(self, obj):
        return self.extra_template.render(obj.extra)
    render_as_html_extra.short_description = _("Details")

    def has_delete_permission(self, request, obj=None):
        return False


#######################################################################
# Produit: Catégorie
#######################################################################


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    ordering_field = "order"
    list_display = [
        "name",
        "parent",
        "order"
    ]
    list_filter = ["parent"]
    list_editable = ["order"]


@admin.register(ProductFilter)
class ProductFilterAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]


@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]

#######################################################################
# Produits
#######################################################################


@admin.register(ProductDefault)
class ProductDefaultAdmin(
    InvalidateProductCacheMixin,
    SortableAdminMixin,
    TranslatableAdmin,
    FrontendEditableAdminMixin,
    PlaceholderAdminMixin,
    PolymorphicChildModelAdmin
):
    base_model = Product
    fieldsets = (
        (None, {
            "fields": [
                ("product_name", "slug"),
                ("product_code", "unit_price", "discounted_price"),
                ("start_date", "end_date"),
                "quantity",
                "active",
                "is_vedette"
            ]
        }),
        (_("Translatable Fields"), {
            "fields": [
                "caption",
                "description"
            ]
        }),
        (_("Categories and Filters"), {
            "fields": [
                "categories",
                "filters"
            ]
        }),
        (_("Brand"), {
            "fields": [
                "brand"
            ]
        }),
        (_("Main Image"), {
            "fields": [
                "main_image"
            ]
        })
    )
    inlines = [ProductImageInline]
    filter_horizontal = ["categories", "filters"]
    readonly_fields = ("slug",)


class ProductVariableVariantInline(admin.TabularInline):
    model = ProductVariableVariant
    extra = 0


@admin.register(ProductVariable)
class ProductVariableAdmin(
    InvalidateProductCacheMixin,
    SortableAdminMixin,
    TranslatableAdmin,
    FrontendEditableAdminMixin,
    PlaceholderAdminMixin,
    PolymorphicChildModelAdmin
):
    base_model = Product
    fieldsets = [
        (None, {
            "fields": [
                ("product_name", "slug"),
                "active",
                "is_vedette"
            ]
        }),
        (_("Translatable Fields"), {
            "fields": [
                "caption",
                "description"
            ]
        }),
        (_("Categories and Filters"), {
            "fields": [
                "categories",
                "filters"
            ]
        }),
        (_("Brand"), {
            "fields": [
                "brand"
            ]
        }),
        (_("Main Image"), {
            "fields": [
                "main_image"
            ]
        })
    ]
    filter_horizontal = ["categories", "filters"]
    inlines = [ProductImageInline, ProductVariableVariantInline]
    readonly_fields = ("slug",)

    def render_text_index(self, instance):
        template = get_template("search/indexes/dshop/commodity_text.txt")
        return template.render(Context({"object": instance}))
    render_text_index.short_description = _("Text Index")


@admin.register(Product)
class ProductAdmin(PolymorphicSortableAdminMixin, PolymorphicParentModelAdmin):
    base_model = Product
    child_models = [ProductDefault, ProductVariable]
    list_display = [
        "product_name",
        "get_price",
        "product_type",
        "get_quantity",
        "is_vedette",
        "active"
    ]
    list_display_links = ["product_name"]
    search_fields = ["product_name"]
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
        except Exception as e:
            print(e)
            result = result.quantity
        return str(result)
    get_quantity.short_description = _("Quantity")


@admin.register(FeatureList)
class FeatureListAdmin(admin.ModelAdmin):

    list_display = ["feature_name", "is_enabled"]
    list_editable = ("is_enabled",)
