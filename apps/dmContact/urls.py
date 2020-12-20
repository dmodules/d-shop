from django.conf.urls import url

from .views import formulaire, infolettre_mailchimp

urlpatterns = [
    url(r'^formulaire/$', formulaire),
    url(r'^infolettre/mailchimp/$', infolettre_mailchimp),
]
