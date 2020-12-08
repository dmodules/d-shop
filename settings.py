INSTALLED_ADDONS = [
    # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    'aldryn-addons',
    'aldryn-django',
    'aldryn-sso',
    'aldryn-django-cms',
    'djangocms-file',
    'djangocms-googlemap',
    'djangocms-history',
    'djangocms-link',
    'djangocms-picture',
    'djangocms-snippet',
    'djangocms-style',
    'djangocms-text-ckeditor',
    'djangocms-video',
    'django-filer',
    # </INSTALLED_ADDONS>
]

import aldryn_addons.settings
aldryn_addons.settings.load(locals())

import os
import six
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _

INSTALLED_APPS.extend([
  "cmsplugin_cascade",
  "cmsplugin_cascade.clipboard",
  "cmsplugin_cascade.sharable",
  "cmsplugin_cascade.extra_fields",
  "cmsplugin_cascade.icon",
  "cmsplugin_cascade.segmentation",
  # ===---
  #'django_elasticsearch_dsl',
  "fsm_admin",
  "adminsortable2",
  # ===---
  "webpack_loader",
  "colorfield",
  # ===---
  "rest_framework",
  "rest_framework.authtoken",
  "rest_auth",
  "post_office",
  # ===---
  "stripe",
  # ===---
  "dshop.dmBillingStripe",
  "dshop.dmContact",
  "dshop.dmRabais",
  "dshop.dmShipping",
  "dshop.dmTaxes",
  # ===---
  "shop",
  "boutique",
  "dmodules"
])

############################################
# Shop Payments and Order Settings

SHOP_VALUE_ADDED_TAX = Decimal(0)
SHOP_DEFAULT_CURRENCY = "CAD"

SHOP_CART_MODIFIERS = [
  "boutique.modifiers.PrimaryCartModifier",
  # ===--- taxes methods
  "dshop.dmTaxes.modifiers.CanadaTaxModifier",
  # ===--- shipping methods
  "dshop.dmShipping.modifiers.FreeShippingModifier",
  "dshop.dmShipping.modifiers.StandardShippingModifier",
  "dshop.dmShipping.modifiers.ExpressShippingModifier",
  # ===--- payment providers
  #"boutique.modifiers.TestPaymentModifier",
  "dshop.dmBillingStripe.modifiers.StripePaymentModifier",
  #"boutique.modifiers.SquarePaymentModifier",
]

SHOP_ORDER_WORKFLOWS = [
  'shop.payment.workflows.ManualPaymentWorkflowMixin',
  #'shop.payment.workflows.CancelOrderWorkflowMixin',
  #'shop.shipping.workflows.SimpleShippingWorkflowMixin',
]

SHOP_CASCADE_FORMS = {
  'CustomerForm': 'boutique.forms.CustomerForm',
}

############################################
# Middleware Settings

MIDDLEWARE.extend([
  'shop.middleware.CustomerMiddleware',
  'django.middleware.security.SecurityMiddleware',
  'django.middleware.gzip.GZipMiddleware',
  'cms.middleware.language.LanguageCookieMiddleware',
  'cms.middleware.user.CurrentUserMiddleware',
  'cms.middleware.page.CurrentPageMiddleware',
  'cms.middleware.utils.ApphookReloadMiddleware',
  'cms.middleware.toolbar.ToolbarMiddleware',
])

STAGE = os.getenv('STAGE', 'local').lower()
CLIENT_SLUG = os.getenv('SITE_NAME', 'd-shop').lower()

#######################################################################
# Actual Shop Settings

SHOP_APP_LABEL = 'boutique'
SITE_ID = 1

CLIENT_TITLE = "D-Shop"
ADMINS = [("D-Modules", 'info@d-modules.com')]
SHOP_VENDOR_EMAIL = 'mariechristine@d-modules.com'

if STAGE == "live":
  SITE_URL = "https://d-shop.us.aldryn.io"
elif STAGE == "test":
  SITE_URL = "https://d-shop-stage.us.aldryn.io"
elif STAGE == "local":
  SITE_URL = "http://localhost:8000"

############################################
# Templates Settings

CMS_TEMPLATES = [
  ("clients/{}/pages/default.html".format(CLIENT_SLUG), "Par défaut"),
  ("clients/{}/pages/accueil.html".format(CLIENT_SLUG), "Page: Accueil"),
  ("clients/{}/pages/produits.html".format(CLIENT_SLUG), "Page: Produits"),
  ("clients/{}/pages/contact.html".format(CLIENT_SLUG), "Page: Contact"),
]

#######################################################################
# Email Settings

EMAIL_HOST = "smtp.mandrillapp.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "mcote@d-modules.com"
EMAIL_HOST_PASSWORD = "15163f93-6766-42b0-b239-6c707093642e"
DEFAULT_FROM_EMAIL = "noreply@d-modules.com"
DEFAULT_TO_EMAIL = "mariechristine@d-modules.com"
EMAIL_REPLY_TO = "info@d-modules.com"
EMAIL_BACKEND = "post_office.EmailBackend"

MAILCHIMP_KEY = "1111111111111111111-11"
MAILCHIMP_LISTID = "1111111111"

#######################################################################
# Stripe Settings

STRIPE_PUBLIC_KEY = "pk_test_oho8Q2pjlnLsmNSkXRT21wi2"
STRIPE_SECRET_KEY = "sk_test_yWfrqAfo9CX6aixqmDoqzeFU"
STRIPE_ACCOUNT_ID = "acct_1DB3G8GqDfDq6eXv"

#######################################################################
# Paths Settings

BASE_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(__file__)

STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')
STATIC_URL = os.environ.get('STATIC_URL', '/static/')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

#######################################################################
# Internationalization

TIME_ZONE = 'America/Toronto'
USE_TZ = True

USE_I18N = True
USE_L10N = True

USE_THOUSAND_SEPARATOR = False

LANGUAGE_CODE = 'fr'
LANGUAGES = [
  ('fr', "French"),
  ('en', "English"),
]
PARLER_DEFAULT_LANGUAGE = 'fr'
PARLER_LANGUAGES = {
  1: [
    {'code': 'fr'},
    {'code': 'en'},
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
    'hide_untranslated': False,
  },
  1: [{
    'public': True,
    'code': 'fr',
    'hide_untranslated': False,
    'name': 'French',
    'redirect_on_fallback': True,
  },{
    'public': True,
    'code': 'en',
    'hide_untranslated': False,
    'name': 'English',
    'redirect_on_fallback': True,
  },]
}

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
      'django.template.context_processors.media',
      'django.template.context_processors.static',
      'django.template.context_processors.tz',
      'django.template.context_processors.csrf',
      'django.template.context_processors.request',
      'django.contrib.messages.context_processors.messages',
      'sekizai.context_processors.sekizai',
      'cms.context_processors.cms_settings',
      'shop.context_processors.customer',
      'shop.context_processors.shop_settings',
    ]
  }
}, {
  'BACKEND': 'post_office.template.backends.post_office.PostOfficeTemplates',
  'APP_DIRS': True,
  'DIRS': [],
  'OPTIONS': {
    'context_processors': [
      'django.contrib.auth.context_processors.auth',
      'django.template.context_processors.debug',
      'django.template.context_processors.i18n',
      'django.template.context_processors.media',
      'django.template.context_processors.static',
      'django.template.context_processors.tz',
      'django.template.context_processors.request',
    ]
  }
}]

#######################################################################
#

POST_OFFICE = {'TEMPLATE_ENGINE': 'post_office'}

#######################################################################
#

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#######################################################################
# settings for caching and storing session data

CACHES = {
  'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'},
  'select2': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}
}

REDIS_HOST = os.getenv('REDIS_HOST')
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
  CACHE_MIDDLEWARE_SECONDS = 1 #3600
else:
  SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

SESSION_SAVE_EVERY_REQUEST = True

LOGGING = {
  'version': 1,
  'disable_existing_loggers': True,
  'filters': {'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}},
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
  'DEFAULT_FILTER_BACKENDS': [
    'django_filters.rest_framework.DjangoFilterBackend'
  ]
}

REST_AUTH_SERIALIZERS = {'LOGIN_SERIALIZER': 'shop.serializers.auth.LoginSerializer'}

############################################
# settings for django-cms and its plugins

from django.urls import reverse_lazy
from django.utils.text import format_lazy
from cmsplugin_cascade.bootstrap4.mixins import BootstrapUtilities
from cmsplugin_cascade.extra_fields.config import PluginExtraFieldsConfig

CMS_PLACEHOLDER_CONF = {
    'Breadcrumb': {
        'plugins': ['BreadcrumbPlugin'],
        'parent_classes': {'BreadcrumbPlugin': None},
    }
}

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
        'ShopAddToCartPlugin': [
            (None, _("Default")),
            ('boutique/catalog/commodity-add2cart.html', _("Add Commodity to Cart")),
        ],
    },
    'plugins_with_sharables': {
        'BootstrapImagePlugin': ['image_shapes', 'image_width_responsive', 'image_width_fixed',
                                 'image_height', 'resize_options'],
        'BootstrapPicturePlugin': ['image_shapes', 'responsive_heights', 'responsive_zoom', 'resize_options'],
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
        'BootstrapYoutubePlugin': BootstrapUtilities(BootstrapUtilities.margins),
        'BootstrapButtonPlugin': BootstrapUtilities(BootstrapUtilities.floats),
    },
    'leaflet': {
        'tilesURL': 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}',
        'accessToken': 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw',
        'apiKey': 'AIzaSyD71sHrtkZMnLqTbgRmY_NsO0A9l9BQmv4',
    },
    'bookmark_prefix': '/',
    'segmentation_mixins': [
        ('shop.cascade.segmentation.EmulateCustomerModelMixin',
         'shop.cascade.segmentation.EmulateCustomerAdminMixin'),
    ],
    'allow_plugin_hiding': True,
}

CKEDITOR_SETTINGS = {
    'language': '{{ language }}',
    'skin': 'moono-lisa',
    'toolbar_CMS': [
        ['Undo', 'Redo'],
        ['cmsplugins', '-', 'ShowBlocks'],
        ['Format'],
        ['TextColor', 'BGColor', '-', 'PasteText', 'PasteFromWord'],
        '/',
        ['Bold', 'Italic', 'Underline', 'Strike', '-',
            'Subscript', 'Superscript', '-', 'RemoveFormat'],
        ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
        ['HorizontalRule'],
        ['NumberedList', 'BulletedList', 'Outdent', 'Indent'],
        ['Source']
    ],
    'stylesSet': format_lazy('default:{}', reverse_lazy('admin:cascade_texteditor_config')),
}

CKEDITOR_SETTINGS_CAPTION = {
    'language': '{{ language }}',
    'skin': 'moono-lisa',
    'height': 70,
    'toolbar_HTMLField': [
        ['Undo', 'Redo'],
        ['Format', 'Styles'],
        ['Bold', 'Italic', 'Underline', '-', 'Subscript',
            'Superscript', '-', 'RemoveFormat'],
        ['Source']
    ],
}

CKEDITOR_SETTINGS_DESCRIPTION = {
    'language': '{{ language }}',
    'skin': 'moono-lisa',
    'height': 250,
    'toolbar_HTMLField': [
        ['Undo', 'Redo'],
        ['cmsplugins', '-', 'ShowBlocks'],
        ['Format', 'Styles'],
        ['TextColor', 'BGColor', '-', 'PasteText', 'PasteFromWord'],
        ['Maximize', ''],
        '/',
        ['Bold', 'Italic', 'Underline', '-', 'Subscript',
            'Superscript', '-', 'RemoveFormat'],
        ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
        ['HorizontalRule'],
        ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
        ['Source']
    ],
}

CKEDITOR_SETTINGS_DMPLUGIN = {
    'language': '{{ language }}',
    'skin': 'moono-lisa',
    'height': 70,
    'toolbar_HTMLField': [
        ['Undo', 'Redo'],
        ['TextColor', 'BGColor'],
        ['Bold', 'Italic', 'Underline', '-', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
        ['Source']
    ],
}

CKEDITOR_SETTINGS_DMBLOCKPLUGIN = {
    'language': '{{ language }}',
    'skin': 'moono-lisa',
    'height': 70,
    'toolbar_HTMLField': [
        ['Undo', 'Redo'],
        ['Format', 'Styles'],
        ['TextColor', 'BGColor'],
        ['Bold', 'Italic', 'Underline', '-', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
        ['HorizontalRule'],
        ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
        ['Source']
    ],
}

SELECT2_CSS = 'node_modules/select2/dist/css/select2.min.css'
SELECT2_JS = 'node_modules/select2/dist/js/select2.min.js'
SELECT2_I18N_PATH = 'node_modules/select2/dist/js/i18n'

#######################################################################
# Full index text search settings

ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'localhost')

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': '{}:9200'.format(ELASTICSEARCH_HOST)
    },
}

#######################################################################
# Frontend Settings

if STAGE == "live" or STAGE == "test":
  STATICFILES_DIRS = STATICFILES_DIRS + ['/app/frontend/bundle/pro']
  VUE_ROOT = os.path.join('/app/frontend/bundle/pro/')
  WEBPACK_LOADER = {
    'DEFAULT': {
      'BUNDLE_DIR_NAME': '',
      'STATS_FILE': '/app/frontend/webpack-pro.json',
    }
  }
if STAGE == 'local':
  STATICFILES_DIRS = STATICFILES_DIRS + ['/app/frontend/bundle/dev']
  VUE_ROOT = os.path.join('/app/frontend/bundle/dev/')
  WEBPACK_LOADER = {
    'DEFAULT': {
      'BUNDLE_DIR_NAME': '',
      'STATS_FILE': '/app/frontend/webpack-dev.json',
    }
  }

#######################################################################
# Admin Reordering

MIDDLEWARE.extend([
  "dmodules.middleware.AdminReorderMiddleware"
])
ADMIN_REORDER = (
  {
    "app":"shop",
    "label":"Site",
    "models":[
      #"sites.Site",
      "boutique.dmSite",
      "cms.Page",
      "shop.CustomerProxy",
      "boutique.dmAlertPublicitaire"
    ]
  },
  {
    "app":"boutique",
    "label": _("Boutique"),
    "models":[
      "boutique.dmRabaisPerCategory",
      "boutique.ProductCategory",
      "boutique.ProductFilter",
      "boutique.Product",
      {"model":"boutique.Order", "label":_("Commandes")},
      {"model":"boutique.Cart", "label":_("Carts")},
      #{"model":"boutique.ShippingAddress", "label":_("Adresses de livraison")},
      #{"model":"boutique.BillingAddress", "label":_("Adresses de facturation")},
    ]
  },
  {
    "app": "dmRabais",
    "label": _("Rabais"),
    "models": [
      "dmRabais.dmRabaisPerCategory",
    ]
  },
  {
    "app": "boutique",
    "label": _("Livraison"),
    "models": [
      "dmShipping.ShippingManagement",
    ]
  },
  {
    "app": "dmTaxes",
    "label": _("Taxes"),
    "models":[
      "dmTaxes.CanadaTaxManagement",
    ]
  },
  {
    "app":"post_office",
    "label": _("Envoi de courriels"),
    "models":[
      "shop.Notification",
      {"model":"post_office.EmailTemplate", "label":_("Gabarits de courriel")},
      {"model":"post_office.Email", "label":_("Courriels envoyés")},
      "post_office.Log"
    ]
  },
  {
    "app":"filer"
  },
)
