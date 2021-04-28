from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class dmAdminThemeConfig(AppConfig):
    name = "apps.dmAdminTheme"
    verbose_name = _("Admin Panel")

    def ready(self):
        import apps.dmAdminTheme.signals  # noqa
