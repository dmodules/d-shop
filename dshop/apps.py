import logging
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class dshopConfig(AppConfig):
    name = "dshop"
    verbose_name = _("Shop")
    logger = logging.getLogger("d-shop")

    def ready(self):
        from shop.models.fields import JSONField
        from rest_framework.serializers import ModelSerializer
        from shop.deferred import ForeignKeyBuilder
        from shop.rest.fields import JSONSerializerField
        from shop.patches import PageAttribute
        from cms.templatetags import cms_tags

        # add JSONField to the map of customized serializers
        ModelSerializer.serializer_field_mapping[
            JSONField] = JSONSerializerField

        # perform some sanity checks
        ForeignKeyBuilder.check_for_pending_mappings()

        cms_tags.register.tags["page_attribute"] = PageAttribute
