from django.utils.translation import gettext_lazy as _
from django.conf import settings

TEMPLATES = {
    ("default.html".format(settings.THEME_SLUG), "Par défaut"),
    ("accueil.html".format(settings.THEME_SLUG), "Page: Accueil"),
    ("produits.html".format(settings.THEME_SLUG), "Page: Produits"),
    ("contact.html".format(settings.THEME_SLUG), "Page: Contact"),
}
