
from django.utils.translation import ugettext_lazy as _
from django.db import models
from filer.fields.file import FilerFileField
from django.template.defaultfilters import slugify

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
