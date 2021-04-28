from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class dmAdminLogs(models.Model):
    CHOIX_ACTION = [
        (0, _("Unknown")),
        (1, _("Created")),
        (2, _("Updated")),
        (3, _("Deleted"))
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="dmadmin_logs",
        verbose_name=_("User"),
        blank=True,
        null=True
    )
    user_action = models.PositiveSmallIntegerField(
        verbose_name=_("Action"),
        choices=CHOIX_ACTION,
        default=0
    )
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=512
    )
    content = models.CharField(
        verbose_name=_("Content"),
        max_length=512
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"),
        auto_now=True,
    )

    class Meta:
        verbose_name = _("Admin Log")
        verbose_name_plural = _("Admin Logs")
        ordering = ["-created_at", "-pk"]

    def __str__(self):
        return "%s" % (str(self.title))
