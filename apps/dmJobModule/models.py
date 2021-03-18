
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.template.defaultfilters import slugify

from djangocms_text_ckeditor.fields import HTMLField

from cms.models import CMSPlugin

from filer.fields.file import FilerFileField

from colorfield.fields import ColorField


class dmJobDescription(models.Model):
    title = models.CharField(
        verbose_name=_("Titre"),
        max_length=250,
        help_text=_("Maximum 250 characters.")
    )
    slug = models.SlugField(
        max_length=200,
        null=True, blank=True
    )
    description = models.TextField(
        verbose_name=_("Description de l'emploi")
    )
    skills = models.CharField(
        verbose_name=_("Compétences"),
        max_length=250,
        null=True, blank=True
    )
    location = models.CharField(
        verbose_name=_("Lieu"),
        max_length=250,
        null=True, blank=True
    )
    salary = models.CharField(
        verbose_name=_("Un salaire"),
        max_length=250,
        null=True, blank=True
    )
    training = models.CharField(
        verbose_name=_("Formation requise?"),
        max_length=100,
        null=True, blank=True
    )
    joining = models.CharField(
        verbose_name=_("Durée prévue de l'adhésion"),
        max_length=250,
        null=True, blank=True
    )
    work_schedule = models.CharField(
        verbose_name=_("Horaire de travail"),
        max_length=100,
        null=True, blank=True
    )
    is_active = models.BooleanField(
        verbose_name=_("Actif"),
        default=True
    )
    created_at = models.DateTimeField(
        verbose_name=_("Créé à"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Mis à jour à"),
        auto_now=True,
    )

    class Meta:
        verbose_name = _("Description de l'emploi")
        verbose_name_plural = _("Description du travail")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(dmJobDescription, self).save(*args, **kwargs)

class dmJobApplication(models.Model):

    job = models.ForeignKey(
        dmJobDescription,
        on_delete=models.CASCADE,
        related_name="job",
    )
    name = models.CharField(
        max_length=250,
        verbose_name=_("Nom")
    )
    email = models.CharField(
        max_length=1000,
        verbose_name=_("E-mail")
    )
    phone = models.CharField(
        max_length=20,
        verbose_name=_("Numéro de téléphone"),
        null=True, blank=True
    )
    message = models.TextField(
        verbose_name=_("Un message")
    )
    document = FilerFileField(
        verbose_name=_("Votre CV"),
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    created_at = models.DateTimeField(
        verbose_name=_("Créé à"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Mis à jour à"),
        auto_now=True,
    )

    class Meta:
        verbose_name = _("Demande d'emploi")
        verbose_name_plural = _("Demandes d'emploi")

    def __str__(self):
        return self.name + " : " + self.email


##############################################################################
# ===---                           PLUGINS                            ---=== #
##############################################################################


class dmJobLastest(CMSPlugin):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Maximum 100 characters.")
    )
    title_color = ColorField(
        verbose_name=_("Title's Colour"),
        null=True,
        blank=True
    )
    text = HTMLField(
        verbose_name=_("Text"),
        configuration="CKEDITOR_SETTINGS_DMPLUGIN",
        null=True,
        blank=True
    )
    text_color = ColorField(
        verbose_name=_("Text's Colour"),
        null=True,
        blank=True
    )
    btn_label = models.CharField(
        verbose_name=_("See All Offers Link's Label"),
        max_length=30,
        default=_("Voir toutes les offres"),
        null=True,
        blank=True,
        help_text=_("Maximum 30 characters.")
    )
    btn_blank = models.BooleanField(
        verbose_name=_("Open on new tab?"),
        default=False
    )
    box_text_color = ColorField(
        verbose_name=_("Box Text's Colour"),
        null=True,
        blank=True
    )
    box_bg_color = ColorField(
        verbose_name=_("Box's Colour"),
        null=True,
        blank=True
    )
    bg_color = ColorField(
        verbose_name=_("Background's Colour"),
        null=True,
        blank=True
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        null=True,
        blank=True,
        help_text=_("Leave blank to hide image.")
    )
