from django.utils.translation import gettext_lazy as _
from django.conf import settings

TEMPLATES = {
    ("default.html".format(settings.CLIENT_SLUG), "Par défaut"),
    ("accueil.html".format(settings.CLIENT_SLUG), "Page: Accueil"),
    ("produits.html".format(settings.CLIENT_SLUG), "Page: Produits"),
    ("contact.html".format(settings.CLIENT_SLUG), "Page: Contact"),
}