import os
import six
import dj_database_url
from decimal import Decimal
from pathlib import Path

from django.urls import reverse_lazy
from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _
from django_storage_url import dsn_configured_storage_class

from cmsplugin_cascade.bootstrap4.mixins import BootstrapUtilities
from cmsplugin_cascade.extra_fields.config import PluginExtraFieldsConfig

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'shop.middleware.CustomerMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
]

ROOT_URLCONF = 'urls'

X_FRAME_OPTIONS = 'SAMEORIGIN'

WSGI_APPLICATION = 'wsgi.application'

DATABASE_URL = os.environ.get('DATABASE_URL',
                              'postgres://postgres@postgres:5432/db')

DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}


'''AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]'''

INSTALLED_APPS = [
    "dal",
    "dal_select2",
    'apps.dmAdminTheme',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'cms',
    'menus',
    'treebeard',
    'sekizai',
    'filer',
    'easy_thumbnails',
    'mptt',
    'parler',
    'polymorphic',
    'django_select2',
    'djangocms_file',
    'djangocms_googlemap',
    'djangocms_history',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_snippet',
    'djangocms_style',
    'djangocms_text_ckeditor',
    'djangocms_video',
]

INSTALLED_APPS.extend([  # noqa: F821
    # ===---
    "cmsplugin_cascade",
    "cmsplugin_cascade.clipboard",
    "cmsplugin_cascade.sharable",
    "cmsplugin_cascade.extra_fields",
    "cmsplugin_cascade.icon",
    "cmsplugin_cascade.segmentation",
    # ===---
    "cities_light",
    "fsm_admin",
    "adminsortable2",
    "sass_processor",
    # ===---
    "webpack_loader",
    "colorfield",
    # ===---
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_auth",
    "post_office",
    # ===---
    "stripe",
    "haystack",
    # ===---
    "apps.dmAdvertising",
    "apps.dmBillingStripe",
    "apps.dmBillingSquare",
    "apps.dmSquare",
    "apps.dmContact",
    "apps.dmRabais",
    "apps.dmShipping",
    "apps.dmTaxes",
    "apps.dmSearch",
    "apps.dmQuotation",
    # ===---
    "shop",
    "dshop",
])

path_to_extended = '/app/extended_apps/'
EXTENDED_APP_DIR = 'extended_apps'  # Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
# DEFAULT_FILE_STORAGE is configured using DEFAULT_STORAGE_DSN

# read the setting value from the environment variable
DEFAULT_STORAGE_DSN = os.environ.get('DEFAULT_STORAGE_DSN')

# dsn_configured_storage_class() requires the name of the setting
DefaultStorageClass = dsn_configured_storage_class('DEFAULT_STORAGE_DSN')

# Django's DEFAULT_FILE_STORAGE requires the class name
DEFAULT_FILE_STORAGE = 'settings.DefaultStorageClass'

# only required for local file storage and serving, in development
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join('/data/media/')

THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE

if os.path.exists(path_to_extended):
    for item in os.listdir(path_to_extended):
        app = ".".join([EXTENDED_APP_DIR, str(item)])
        app_path = os.path.join(path_to_extended, item)
        if os.path.isdir(app_path) and app not in INSTALLED_APPS:  # noqa: F821
            INSTALLED_APPS.append(app)  # noqa: F821

############################################

CITIES_LIGHT_CITY_SOURCES = [
    'http://download.geonames.org/export/dump/cities500.zip'
]

# Shop Payments and Order Settings

SHOP_VALUE_ADDED_TAX = Decimal(0)
SHOP_DEFAULT_CURRENCY = "CAD"

SHOP_CART_MODIFIERS = [
    "dshop.modifiers.PrimaryCartModifier",
    # ===--- discounts methods
    "apps.dmRabais.modifiers.DiscountsModifier",
    # ===--- shipping methods
    "apps.dmShipping.modifiers.PickupShippingModifier",
    "apps.dmShipping.modifiers.FreeShippingModifier",
    "apps.dmShipping.modifiers.StandardShippingModifier",
    "apps.dmShipping.modifiers.ExpressShippingModifier",
    "apps.dmShipping.modifiers.StandardShippingWithSeparatorModifier",
    "apps.dmShipping.modifiers.ExpressShippingWithSeparatorModifier",
    # ===--- taxes methods
    "apps.dmTaxes.modifiers.CanadaTaxModifier",
]

SHOP_ORDER_WORKFLOWS = [
    "shop.payment.workflows.ManualPaymentWorkflowMixin",
    "shop.shipping.workflows.PartialDeliveryWorkflowMixin"
]

SHOP_CASCADE_FORMS = {
    "CustomerForm": "dshop.forms.CustomerForm",
}

############################################
# Middleware Settings

STAGE = os.getenv("STAGE", "local").lower()

#######################################################################
# Actual Shop Settings

SHOP_APP_LABEL = "dshop"
SITE_ID = 1

CLIENT_TITLE = os.getenv("CLIENT_TITLE", "D-Shop")
SHOP_VENDOR_EMAIL = os.getenv("SHOP_VENDOR_EMAIL")
CC_EMAILS = os.getenv("CC_EMAILS")
ADMINS = [("D-Modules", "info@d-modules.com")]

ORDER_TIMEOUT = os.getenv("ORDER_TIMEOUT", 10)

SHOP_PRODUCT_SUMMARY_SERIALIZER = "dshop.serializers.dmProductSummarySerializer" # noqa

############################################
# Templates Settings

THEME_SLUG = "default"

TEMPLATE_DIR = "theme/default/pages/"

CMS_TEMPLATES = [
    ("theme/default/pages/default.html", "Par défaut"),
    ("theme/default/pages/accueil.html", "Page: Accueil"),
    ("theme/default/pages/produits.html", "Page: Produits"),
    ("theme/default/pages/terms-and-conditions.html",
     "Page: Terms and Conditions"),
    ("theme/default/pages/contact.html", "Page: Contact"),
]

#######################################################################
# Email Settings

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
DEFAULT_TO_EMAIL = os.getenv("DEFAULT_TO_EMAIL")
EMAIL_REPLY_TO = "info@d-modules.com"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = "post_office.EmailBackend"

#######################################################################
# Mailchimp Settings

MAILCHIMP_KEY = os.getenv("MAILCHIMP_KEY")
MAILCHIMP_LISTID = os.getenv("MAILCHIMP_LISTID")

#######################################################################
# ReCaptcha Settings

RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

#######################################################################
# Stripe Settings

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
STRIPE_ACCOUNT_ID = os.getenv("STRIPE_ACCOUNT_ID")

if STRIPE_SECRET_KEY is not None:
    SHOP_CART_MODIFIERS.extend(
        ["apps.dmBillingStripe.modifiers.StripePaymentModifier"])

#######################################################################
# Feature Settings

FEATURES = os.getenv("FEATURES", "")

#######################################################################
# Square Settings

SQUARE_SYNC = os.getenv("SQUARE_SYNC", "1")
SQUARE_APIKEY = os.getenv("SQUARE_APIKEY")
SQUARE_TOKEN = os.getenv("SQUARE_TOKEN")
SQUARE_LOCATION_ID = os.getenv("SQUARE_LOCATION_ID")
SQUARE_ENVIRONMENT = os.getenv("SQUARE_ENVIRONMENT")

if SQUARE_APIKEY is not None:
    SHOP_CART_MODIFIERS.extend(
        ["apps.dmBillingSquare.modifiers.SquarePaymentModifier"])

USE_THOUSAND_SEPARATOR = False

LANGUAGE_CODE = 'fr'
LANGUAGES = [
    ('fr', _("French")),
    ('en', _("English")),
]
PARLER_DEFAULT_LANGUAGE = 'fr'
PARLER_LANGUAGES = {
    1: [
        {
            'code': 'fr'
        },
        {
            'code': 'en'
        },
    ],
    'default': {
        'fallbacks': ['fr', 'en'],
    },
}
CMS_LANGUAGES = {
    'default': {
        'fallbacks': ['fr', 'en'],
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': True,
    },
    1: [
        {
            'public': True,
            'code': 'fr',
            'hide_untranslated': False,
            'name': _("French"),
            'redirect_on_fallback': True,
        },
        {
            'public': True,
            'code': 'en',
            'hide_untranslated': True,
            'name': _("English"),
            'redirect_on_fallback': True,
        },
    ]
}

LOCALE_PATHS = [
    os.path.join("/app/locale")
]

#######################################################################
#

ROBOTS_META_TAGS = ["Allow"]

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'DIRS': ['templates/'],
    'OPTIONS': {
        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.tz',
            'django.template.context_processors.csrf',
            'django.template.context_processors.request',
            'django.contrib.messages.context_processors.messages',
            'sekizai.context_processors.sekizai',
            'cms.context_processors.cms_settings',
            'shop.context_processors.customer',
            'shop.context_processors.shop_settings'
        ]
    }
}]

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    # 'easy_thumbnails.processors.scale_and_crop',
    'easy_thumbnails.processors.filters',
    'easy_thumbnails.processors.background',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location'
)

AUTH_PASSWORD_VALIDATORS = [{
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    'OPTIONS': {
        'min_length': 6,
    }
}]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

#######################################################################
#

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#######################################################################
#

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.simple_backend.SimpleEngine",
    },
}

#######################################################################
# settings for caching and storing session data

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    },
    'select2': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    }
}

REDIS_HOST = os.getenv("REDIS_HOST")
if REDIS_HOST:
    SESSION_ENGINE = 'redis_sessions.session'
    SESSION_REDIS = {
        'host': REDIS_HOST,
        'port': 6379,
        'db': 0,
        'prefix': 'session-',
        'socket_timeout': 1
    }
    CACHES['default'] = {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'redis://{}:6379/1'.format(REDIS_HOST),
        'OPTIONS': {
            'PICKLE_VERSION': 2 if six.PY2 else -1,
        }
    }
    CACHE_MIDDLEWARE_ALIAS = 'default'
    CACHE_MIDDLEWARE_SECONDS = 1  # 3600
else:
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

SESSION_SAVE_EVERY_REQUEST = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'simple': {
            'format': '[%(asctime)s %(module)s] %(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'post_office': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

SILENCED_SYSTEM_CHECKS = ['auth.W004']

#######################################################################
# 3-party django apps Settings

COERCE_DECIMAL_TO_STRING = True
FSM_ADMIN_FORCE_PERMIT = True
SERIALIZATION_MODULES = {'json': str('shop.money.serializers')}

FILER_FILE_MODELS = [
    "filer.Image",
    "filer.File",
]

#######################################################################
# REST Settings

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'shop.rest.money.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ],
    'DEFAULT_FILTER_BACKENDS':
    ['django_filters.rest_framework.DjangoFilterBackend']
}

REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'shop.serializers.auth.LoginSerializer'
}

############################################
# settings for django-cms and its plugins

CMSPLUGIN_CASCADE_PLUGINS = [
    'cmsplugin_cascade.bootstrap4',
    'cmsplugin_cascade.segmentation',
    'cmsplugin_cascade.generic',
    'cmsplugin_cascade.icon',
    'cmsplugin_cascade.leaflet',
    'cmsplugin_cascade.link',
    'shop.cascade',
]

CMSPLUGIN_CASCADE = {
    'link_plugin_classes': [
        'shop.cascade.plugin_base.CatalogLinkPluginBase',
        'shop.cascade.plugin_base.CatalogLinkForm',
    ],
    'alien_plugins': ['TextPlugin', 'TextLinkPlugin', 'AcceptConditionPlugin'],
    'bootstrap4': {
        'template_basedir': 'angular-ui/',
    },
    'plugins_with_extra_render_templates': {
        'CustomSnippetPlugin': [
            ('shop/catalog/product-heading.html', _("Product Heading")),
        ],
        # required to purchase real estate
        'ShopAddToCartPlugin': [(None, _("Default"))],
    },
    'plugins_with_sharables': {
        'BootstrapImagePlugin': [
            'image_shapes', 'image_width_responsive', 'image_width_fixed',
            'image_height', 'resize_options'
        ],
        'BootstrapPicturePlugin': [
            'image_shapes', 'responsive_heights', 'responsive_zoom',
            'resize_options'
        ],
    },
    'plugins_with_extra_fields': {
        'BootstrapCardPlugin': PluginExtraFieldsConfig(),
        'BootstrapCardHeaderPlugin': PluginExtraFieldsConfig(),
        'BootstrapCardBodyPlugin': PluginExtraFieldsConfig(),
        'BootstrapCardFooterPlugin': PluginExtraFieldsConfig(),
        'SimpleIconPlugin': PluginExtraFieldsConfig(),
    },
    'plugins_with_extra_mixins': {
        'BootstrapContainerPlugin': BootstrapUtilities(),
        'BootstrapRowPlugin': BootstrapUtilities(BootstrapUtilities.paddings),
        'BootstrapYoutubePlugin':
        BootstrapUtilities(BootstrapUtilities.margins),
        'BootstrapButtonPlugin': BootstrapUtilities(BootstrapUtilities.floats),
    },
    'leaflet': {
        'tilesURL':
        'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', # noqa
        'accessToken':
        'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', # noqa
        'apiKey': 'AIzaSyD71sHrtkZMnLqTbgRmY_NsO0A9l9BQmv4',
    },
    'bookmark_prefix':
    '/',
    'segmentation_mixins': [
        ('shop.cascade.segmentation.EmulateCustomerModelMixin',
         'shop.cascade.segmentation.EmulateCustomerAdminMixin'),
    ],
    'allow_plugin_hiding':
    True,
}

CKEDITOR_SETTINGS = {
    'language':
    '{{ language }}',
    'skin':
    'moono-lisa',
    'toolbar_CMS':
    [['Undo', 'Redo'], ['cmsplugins', 'ShowBlocks'],
     ['Format', 'Styles', 'FontSize'],
     ['TextColor', 'BGColor', '-', 'Link', '-', 'PasteText', 'PasteFromWord'],
     ['Maximize', ''], '/',
     [
         'Bold', 'Italic', 'Underline', 'Strike', '-', 'Subscript',
         'Superscript', '-', 'RemoveFormat'
     ], ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
     ['HorizontalRule'], ['NumberedList', 'BulletedList', 'Outdent', 'Indent'],
     ['Source']],
    'stylesSet':
    format_lazy('default:{}', reverse_lazy('admin:cascade_texteditor_config')),
}

CKEDITOR_SETTINGS_CAPTION = {
    'language':
    '{{ language }}',
    'skin':
    'moono-lisa',
    'height':
    250,
    'toolbar_HTMLField':
    [['Undo', 'Redo'], ['cmsplugins', 'ShowBlocks'],
     ['Format', 'Styles', 'FontSize'],
     ['TextColor', 'BGColor', '-', 'Link', '-', 'PasteText', 'PasteFromWord'],
     ['Maximize', ''], '/',
     [
         'Bold', 'Italic', 'Underline', 'Strike', '-', 'Subscript',
         'Superscript', '-', 'RemoveFormat'
     ], ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
     ['HorizontalRule'], ['NumberedList', 'BulletedList', 'Outdent', 'Indent'],
     ['Source']]
}

CKEDITOR_SETTINGS_DESCRIPTION = {
    'language':
    '{{ language }}',
    'skin':
    'moono-lisa',
    'height':
    250,
    'toolbar_HTMLField':
    [['Undo', 'Redo'], ['cmsplugins', 'ShowBlocks'],
     ['Format', 'Styles', 'FontSize'],
     ['TextColor', 'BGColor', '-', 'Link', '-', 'PasteText', 'PasteFromWord'],
     ['Maximize', ''], '/',
     [
         'Bold', 'Italic', 'Underline', 'Strike', '-', 'Subscript',
         'Superscript', '-', 'RemoveFormat'
     ], ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
     ['HorizontalRule'], ['NumberedList', 'BulletedList', 'Outdent', 'Indent'],
     ['Source']]
}

CKEDITOR_SETTINGS_DMPLUGIN = {
    'language':
    '{{ language }}',
    'skin':
    'moono-lisa',
    'height':
    250,
    'toolbar_HTMLField':
    [['Undo', 'Redo'], ['cmsplugins', 'ShowBlocks'],
     ['Format', 'Styles', 'FontSize'],
     ['TextColor', 'BGColor', '-', 'Link', '-', 'PasteText', 'PasteFromWord'],
     ['Maximize', ''], '/',
     [
         'Bold', 'Italic', 'Underline', 'Strike', '-', 'Subscript',
         'Superscript', '-', 'RemoveFormat'
     ], ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
     ['HorizontalRule'], ['NumberedList', 'BulletedList', 'Outdent', 'Indent'],
     ['Source']]
}

CKEDITOR_SETTINGS_DMBLOCKPLUGIN = {
    'language':
    '{{ language }}',
    'skin':
    'moono-lisa',
    'height':
    250,
    'toolbar_HTMLField':
    [['Undo', 'Redo'], ['cmsplugins', 'ShowBlocks'],
     ['Format', 'Styles', 'FontSize'],
     ['TextColor', 'BGColor', '-', 'Link', '-', 'PasteText', 'PasteFromWord'],
     ['Maximize', ''], '/',
     [
         'Bold', 'Italic', 'Underline', 'Strike', '-', 'Subscript',
         'Superscript', '-', 'RemoveFormat'
     ], ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
     ['HorizontalRule'], ['NumberedList', 'BulletedList', 'Outdent', 'Indent'],
     ['Source']]
}

# SELECT2_CSS = 'node_modules/select2/dist/css/select2.min.css'
# SELECT2_JS = 'node_modules/select2/dist/js/select2.min.js'
# SELECT2_I18N_PATH = 'node_modules/select2/dist/js/i18n'

STATICFILES_DIRS = [
    # ('node_modules', os.path.join(BASE_DIR, 'node_modules')),
    os.path.join("/app/static")
]

#######################################################################
# Full index text search settings

ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "localhost")

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': '{}:9200'.format(ELASTICSEARCH_HOST)
    },
}

#######################################################################
# Frontend Settings

if STAGE == "live" or STAGE == "test":
    STATICFILES_DIRS += ['/app/frontend/bundle/pro']
    VUE_ROOT = os.path.join('/app/frontend/bundle/pro/')
    WEBPACK_LOADER = {
        'DEFAULT': {
            'BUNDLE_DIR_NAME': '',
            'STATS_FILE': '/app/frontend/webpack-pro.json',
        }
    }
if STAGE == 'local':
    STATICFILES_DIRS += ['/app/frontend/bundle/dev']
    VUE_ROOT = os.path.join('/app/frontend/bundle/dev/')
    WEBPACK_LOADER = {
        'DEFAULT': {
            'BUNDLE_DIR_NAME': '',
            'STATS_FILE': '/app/frontend/webpack-dev.json',
        }
    }

#######################################################################
# Admin Reordering

MIDDLEWARE.extend(["dshop.middleware.AdminReorderMiddleware"])  # noqa: F821
TEMP_ADMIN_REORDER = [
    {
        "app":
        "shop",
        "label":
        "Site",
        "models": [
            "dshop.dmSite",
            "cms.Page",
            "shop.CustomerProxy",
            "dshop.FeatureList",
        ]
    },
    {
        "app": "dmAdvertising",
        "label": _("Advertising")
    },
    {
        "app":
        "dshop",
        "label":
        _("Shop"),
        "models": [
            "dshop.ProductCategory",
            "dshop.ProductFilter",
            "dshop.ProductBrand",
            "dshop.Attribute",
            "dshop.ProductVariableVariant",
            "dshop.Product",
            {
                "model": "dshop.Order",
                "label": _("Orders")
            },
            {
                "model": "dshop.Delivery",
                "label": _("Delivery")
            },
            {
                "model": "dshop.DeliveryItem",
                "label": _("DeliveryItem")
            },
            # {"model": "dshop.Cart", "label": _("Carts")},
            # {"model": "dshop.ShippingAddress", "label":_("Shipping's Addresses")}, # noqa
            # {"model": "dshop.BillingAddress", "label":_("Billing's Addresses")}, # noqa
        ]
    },
    {
        "app":
        "dmRabais",
        "label":
        _("Discounts"),
        "models": [
            "dmRabais.dmRabaisPerCategory",
            "dmRabais.dmPromoCode",
            # "dmRabais.dmCustomerPromoCode"
        ]
    },
    {
        "app":
        "dshop",
        "label":
        _("Shipping"),
        "models": [
            "dmShipping.ShippingManagement",
            "dmShipping.ShippingCountry",
            "dmShipping.ShippingState",
            "dmShipping.ShippingCity",
            "dmShipping.ShippingAllowed",
        ]
    },
    {
        "app": "dmTaxes",
        "label": _("Taxes"),
        "models": [
            "dmTaxes.CanadaTaxManagement",
        ]
    },
    {
        "app":
        "post_office",
        "label":
        _("Sending Emails"),
        "models": [
            "shop.Notification", {
                "model": "post_office.EmailTemplate",
                "label": _("Email Templates")
            }, {
                "model": "post_office.Email",
                "label": _("Sent Emails")
            }, "post_office.Log"
        ]
    },
    {
        "app": "dmTheme",
        "label": _("Theme Management"),
        "models": [
            "dmTheme.ThemeManagement",
        ]
    },
    {
        "app": "dmSquare"
    },
    {
        "app": "filer"
    },
    {
        "app": "cities_light"
    },
]

if 'QUOTATION' in FEATURES:
    TEMP_ADMIN_REORDER.append({"app": "dmQuotation"})
if os.path.exists(path_to_extended):
    for item in os.listdir(path_to_extended):
        app = ".".join([EXTENDED_APP_DIR, str(item)])
        app_path = os.path.join(path_to_extended, item)
        admin_file = os.path.join(app_path, '.admin')
        if os.path.exists(admin_file):
            data = {"app": item}
            TEMP_ADMIN_REORDER.append(data)

ADMIN_REORDER = tuple(TEMP_ADMIN_REORDER)

if STAGE != 'local':
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn= # noqa
        "https://34444139af8548e99bce82a828909a20@o517405.ingest.sentry.io/5625175", # noqa
        integrations=[DjangoIntegration()],
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        debug=os.environ.get('DEBUG') == "True",
        release=os.getenv('GIT_COMMIT', 'develop'),
        environment=os.getenv('STAGE', 'local'),
        send_default_pii=True)

email_path = os.path.join('theme', THEME_SLUG, 'email')

NOTIFICATION_TARGET = {
    'payment_confirmed': {
        'email_template_vendor':
        os.path.join(email_path, 'vendor_order_receipt.html'),
        'email_template_customer':
        os.path.join(email_path, 'customer_order_receipt.html'),
        'to_vendor':
        True,
        'to_customer':
        True,
        'cc_emails':
        True
    },
    'ready_for_delivery': {
        'email_template': os.path.join(email_path,
                                       'customer_shipped_receipt.html'),
        'to_vendor': False,
        'to_customer': True,
        'cc_emails': True
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '4zivFCodJW7ku6h6dyeA')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == "True"

DIVIO_DOMAIN = os.environ.get('DOMAIN', '')
DIVIO_DOMAIN_ALIASES = [
    d.strip() for d in os.environ.get('DOMAIN_ALIASES', '').split(',')
    if d.strip()
]
DIVIO_DOMAIN_REDIRECTS = [
    d.strip() for d in os.environ.get('DOMAIN_REDIRECTS', '').split(',')
    if d.strip()
]

ALLOWED_HOSTS = [DIVIO_DOMAIN] + DIVIO_DOMAIN_ALIASES + DIVIO_DOMAIN_REDIRECTS

# Redirect to HTTPS by default, unless explicitly disabled
# SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT') != "False"
SECURE_SSL_REDIRECT = False

SELECT2_CACHE_BACKEND = "select2"
