from django.utils.translation import gettext_lazy as _
TEMPLATES = {
    ("default.html".format(CLIENT_SLUG), "Par défaut"),
    ("accueil.html".format(CLIENT_SLUG), "Page: Accueil"),
    ("produits.html".format(CLIENT_SLUG), "Page: Produits"),
    ("contact.html".format(CLIENT_SLUG), "Page: Contact"),
}