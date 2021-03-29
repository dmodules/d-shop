import pytz

from datetime import datetime, timedelta

from django.utils.html import mark_safe
from django import forms
from django.contrib import admin
from django.template.context import Context
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse, NoReverseMatch
from django.utils.html import format_html
from django.forms.models import BaseInlineFormSet
from django.db.models import Q

from dal import autocomplete

from mptt.admin import DraggableMPTTAdmin

from cms.admin.placeholderadmin import PlaceholderAdminMixin
from cms.admin.placeholderadmin import FrontendEditableAdminMixin

from adminsortable2.admin import SortableAdminMixin

from polymorphic.admin import (
    PolymorphicParentModelAdmin,
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter
)

from parler.admin import TranslatableAdmin, TranslatableTabularInline

from filer.models import ThumbnailOption

from shop.admin.defaults import customer
from shop.admin.product import ProductImageInline
from shop.admin.product import InvalidateProductCacheMixin
from shop.admin.defaults.order import OrderAdmin as djOrderAdmin
from shop.admin.order import OrderItemInline
from shop.models.defaults.order import Order
from shop.models.cart import CartModel, CartItemModel

from dshop.models import dmSite, dmSiteLogo, dmSiteContact, dmSiteSocial
from dshop.models import dmSiteTermsAndConditions
from dshop.models import BillingAddress, ShippingAddress
from dshop.models import ProductCategory, ProductFilter, ProductBrand, ProductLabel
from dshop.models import Product, ProductDocument
from dshop.models import Product, ProductFilterGroup
from dshop.models import Attribute, AttributeValue
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


class dmSiteContactInline(admin.StackedInline):
    model = dmSiteContact
    extra = 1
    max_num = 1
    fields = [
        ("phone", "phone_secondary"),
        ("email"),
        ("address"),
        ("schedule")
    ]


class dmSiteSocialInline(admin.TabularInline):
    model = dmSiteSocial
    extra = 1


class dmSiteTermsAndConditionsInline(TranslatableTabularInline):
    model = dmSiteTermsAndConditions
    extra = 1
    max_num = 1


@admin.register(dmSite)
class dmSiteAdmin(admin.ModelAdmin):
    list_display = ["get_name", "site"]
    inlines = [
        dmSiteLogoInline,
        dmSiteContactInline,
        dmSiteSocialInline,
        dmSiteTermsAndConditionsInline
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

@admin.register(CartModel)
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
class OrderAdmin(DeliveryOrderAdminMixin, djOrderAdmin):
    list_filter = []
    list_display = [
        "get_number",
        "get_customer",
        "get_status",
        "get_total",
        "created_at"
    ]
    fields = [
        "get_ordernumber",
        "get_customer",
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
        "get_customer",
        "get_outstanding_amount",
        "updated_at",
        "render_as_html_extra",
        "stored_request",
        "is_fully_paid"
    ]
    ordering = ["-created_at"]
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

    def get_customer(self, obj):
        try:
            url = reverse('admin:shop_customerproxy_change', args=(obj.customer.pk,))
            return format_html('<a href="{0}" target="_new">{1}</a>', url, obj.customer.email)
        except NoReverseMatch:
            return format_html('<strong>{0}</strong>', obj.customer.email)
    get_customer.short_description = _("Customer")

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
class ProductCategoryAdmin(DraggableMPTTAdmin):
    pass


class ProductFilterInline(admin.TabularInline):
    model = ProductFilter
    extra = 0

@admin.register(ProductFilterGroup)
class ProductFilterGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
    list_editable = ["order"]
    inlines = [ProductFilterInline]


@admin.register(ProductFilter)
class ProductFilterAdmin(admin.ModelAdmin):
    list_display = ["name", "group", "order"]
    list_editable = ["order"]


@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]


@admin.register(ProductLabel)
class ProductLabelAdmin(admin.ModelAdmin):
    list_display = ["name"]


#######################################################################
# Documents
#######################################################################


class ProductDocumentInline(admin.TabularInline):
    model = ProductDocument
    extra = 0


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
        (None, {
            "fields": [
                "brand"
            ]
        }),
        (None, {
            "fields": [
                "label"
            ]
        }),
        (_("Main Image"), {
            "fields": [
                "main_image"
            ]
        })
    )
    inlines = [ProductImageInline, ProductDocumentInline]
    filter_horizontal = ["categories", "filters"]
    readonly_fields = ("slug",)

class ProductForm(forms.models.ModelForm):
    class Meta:
        model = ProductVariableVariant
        fields = '__all__'
        widgets = {
            'attribute': autocomplete.ModelSelect2Multiple(url='attribute-autocomplete')
        }

class VariantInlineFormSet(BaseInlineFormSet):
   def clean(self):  
        check_data = []
        flag = False
        for form in self.forms:
            is_valid = []
            for attr in form.cleaned_data['attribute']:
                if attr.attribute.name not in is_valid:
                    is_valid.append(attr.attribute.name)
                else:
                    flag = True
                    message = _("You can not select same Attribute type for one variant")
                    break
            if flag:
                break
            if not check_data:
                check_data = is_valid
            if check_data != is_valid:
                flag = True
                message = _("You need to select same Attribute type for all variant")
                break
        if flag:
            raise forms.ValidationError(message)

class ProductVariableVariantInline(admin.TabularInline):
    model = ProductVariableVariant
    extra = 0
    form = ProductForm
    formset = VariantInlineFormSet

@admin.register(ProductVariableVariant)
class ProductVariableVariantAdmin(admin.ModelAdmin):

    search_fields = ['product_code',
                     'product__product_name']

    list_display = [
        'get_product_name',
        'product_code',
        'get_attribute',
        'unit_price',
        'quantity'
    ]

    list_editable = ['quantity']

    def get_product_name(self, obj):
        url = '/admindshop/product/' + str(obj.product.id) 
        tag = '<a href="' + url + '/">' + obj.product.product_name + '</a>'
        return mark_safe(tag)
    get_product_name.short_description = _("Product Name")

    def get_attribute(self, obj):
        attrs = "<br>".join([atr.attribute.name + " : " + atr.value for atr in obj.attribute.all()])
        return mark_safe(attrs)
    get_attribute.short_description = _("Attributes")

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
        (None, {
            "fields": [
                "brand"
            ]
        }),
        (None, {
            "fields": [
                "label"
            ]
        }),
        (_("Main Image"), {
            "fields": [
                "main_image"
            ]
        })
    ]
    filter_horizontal = ["categories", "filters"]
    inlines = [ProductImageInline, ProductDocumentInline, ProductVariableVariantInline]
    readonly_fields = ("slug",)

    def render_text_index(self, instance):
        template = get_template("search/indexes/dshop/commodity_text.txt")
        return template.render(Context({"object": instance}))
    render_text_index.short_description = _("Text Index")


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 0
    exclude = ['square_id']

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):

    list_display = ['name', 'value_display']
    inlines = [AttributeValueInline]
    exclude = ['square_id']

    def value_display(self, obj):
        return ", ".join([
            val.value for val in AttributeValue.objects.filter(attribute=obj)
        ])

def convert_variable(modeladmin, request, queryset):
    for product in queryset:
        if product.product_model == "productdefault":
            print(product.id)
            product = ProductDefault.objects.get(id=product.id)
            last_id = Product.objects.all().order_by('id').last().id + 1
            try:
                data = {
                    'id': last_id,
                    'product_name': product.product_name,
                    'description': product.description,
                    'caption': product.caption,
                    'main_image': product.main_image,
                    'active': product.active,
                    'is_vedette': product.is_vedette,
                    'order': product.order
                }
                v_product = ProductVariable.objects.create(**data)
            except Exception as e:
                print("Exception in product variable")
                print(e)
                continue
            # Add categories
            for cat in product.categories.all():
                v_product.categories.add(cat)
            # Add filters
            for filt in product.filters.all():
                v_product.filters.add(filt)
            try:
                data = {
                    'product': v_product,
                    'product_code': product.product_code,
                    'unit_price': product.unit_price,
                    'discounted_price': product.discounted_price,
                    'start_date': product.start_date,
                    'end_date': product.end_date,
                    'quantity': product.quantity
                }
                ProductVariableVariant.objects.create(**data)
                product.delete()
            except Exception as e:
                print("Exception in product variable variant.")
                print(e)
                v_product.delete()


convert_variable.short_description = _('Convertir en variable')


####################################################################################


class GetProductOutOrLow(admin.SimpleListFilter):
    title = _("Low or Out of Stock")
    parameter_name = "get_product_out_or_low"

    def lookups(self, request, model_admin):
        return (
            ("outofstock", _("Out of stock")),
            ("lowonstock", _("Low on stock")),
        )

    def queryset(self, request, queryset):
        value = self.value()
        result = Product.objects.none()
        if value == "outofstock":
            for p in queryset:
                if p.polymorphic_ctype_id == 163 and p.productdefault.quantity == 0:
                    result |= Product.objects.filter(pk=p.pk)
                elif p.polymorphic_ctype_id == 164:
                    for v in p.productvariable.variants.all():
                        if v.quantity == 0:
                            result |= Product.objects.filter(pk=p.pk)
        elif value == "lowonstock":
            for p in queryset:
                if p.polymorphic_ctype_id == 163 and p.productdefault.quantity <= 3 and p.productdefault.quantity > 0:
                    result |= Product.objects.filter(pk=p.pk)
                elif p.polymorphic_ctype_id == 164:
                    for v in p.productvariable.variants.all():
                        if v.quantity <= 3 and v.quantity > 0:
                            result |= Product.objects.filter(pk=p.pk)
        else:
            result = queryset
        return result.distinct()


@admin.register(Product)
class ProductAdmin(PolymorphicParentModelAdmin):
    base_model = Product
    child_models = [ProductDefault, ProductVariable]
    list_display = [
        "product_name",
        "brand",
        "label",
        # "get_price",
        # "product_type",
        "get_quantity",
        "created_at",
        "is_vedette",
        "active"
    ]
    actions = [convert_variable, ]
    list_display_links = ["product_name"]
    search_fields = ["product_name"]
    list_filter = ["categories", "brand", "label", GetProductOutOrLow, PolymorphicChildModelFilter]
    list_per_page = 100
    list_max_show_all = 1000
    list_editable = ["brand", "label", "active", "is_vedette"]


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
        except Exception:
            # print(e)
            result = result.quantity
        return str(result)
    get_quantity.short_description = _("Quantity")


@admin.register(FeatureList)
class FeatureListAdmin(admin.ModelAdmin):

    list_display = ["feature_name", "is_enabled"]
    list_editable = ("is_enabled",)

