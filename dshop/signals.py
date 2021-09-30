from django.dispatch import receiver
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from settings import THEME_SLUG

from cms.models import Page, Title
from cms.api import create_page, create_title, publish_page

from parler.signals import post_translation_save

from .models import dmSiteTermsAndConditions


@receiver(post_translation_save, sender=dmSiteTermsAndConditions)
def handle_termsandconditions(sender, instance, **kwargs):
    pages = Page.objects.filter(reverse_id="terms-and-conditions")
    translation.activate(instance.language_code)
    trans_title = str(_("Terms and Conditions"))
    translation.deactivate()
    if pages.count() == 0:
        data = {
            "title": str(trans_title),
            "template": "theme/"+THEME_SLUG+"/pages/terms-and-conditions.html",
            "language": instance.language_code,
            "reverse_id": "terms-and-conditions",
            "published": True,
            "created_by": "Site"
        }
        create_page(**data)
    elif pages.count() > 0:
        if Title.objects.filter(
           page__reverse_id="terms-and-conditions",
           language=instance.language_code
           ).count() == 0:
            data = {
                "language": instance.language_code,
                "title": str(trans_title),
                "page": pages.first()
            }
            create_title(**data)
            publish_page(
                pages.first(),
                User.objects.filter(
                    is_superuser=True
                ).first(),
                instance.language_code
            )
