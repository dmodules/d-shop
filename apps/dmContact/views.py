from mailchimp3 import MailChimp

from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.core.management import call_command
from django.core.mail import send_mail

from settings import DEFAULT_FROM_EMAIL, DEFAULT_TO_EMAIL
from settings import MAILCHIMP_KEY, MAILCHIMP_LISTID

#######################################################################
# ===---   Formulaire
#######################################################################

def formulaire(request):
  send_mail(
    "Message du formulaire de contact de votre site web",
    "Bonjour, voici le message:\n\n"
    + "Nom : " + request.POST.get("name", "-") + "\n"
    + "Courriel : " + request.POST.get("email", "-") + "\n"
    + "Téléphone : " + request.POST.get("phone", "-") + "\n"
    + "Sujet : " + request.POST.get("subject", "-") + "\n"
    + "Message :\n\n" + request.POST.get("message", "-"),
    DEFAULT_FROM_EMAIL,
    [DEFAULT_TO_EMAIL],
    fail_silently = False,
  )
  call_command("send_queued_mail")
  return redirect("/message-envoye/")

#######################################################################
# ===---   Infolettre
#######################################################################

def infolettre_mailchimp(request):
  client = MailChimp(mc_api = MAILCHIMP_KEY)
  email = request.POST.get("email_infolettre", "")
  calcul = request.POST.get("calcul_infolettre", "")
  if calcul == "6":
    try:
      client.lists.members.create(MAILCHIMP_LISTID, {
        "email_address": email,
        "status": "subscribed",
      })
      messages.success(request, _("Vous avez bien été ajouté à notre liste de courriels."))
    except:
      messages.error(request, _("Oups, il y a un problème avec votre inscription."))
      redirect("/")
  else:
    messages.error(request, _("La réponse du calcul est incorrecte."))
  return redirect("/")
