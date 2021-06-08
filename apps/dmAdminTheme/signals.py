import inspect

from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from django.db.models.signals import pre_save, post_save, post_delete

from dshop.models import ProductDefault, ProductVariable, ProductVariableVariant
from dshop.models import ProductCategory, ProductBrand, ProductLabel
from dshop.models import ProductFilterGroup, ProductFilter
from dshop.models import Order

from apps.dmRabais.models import dmRabaisPerCategory, dmPromoCode

from apps.dmAdvertising.models import dmAdvertisingTopBanner, dmAdvertisingPopup

from .models import dmAdminLogs


def create_log(user, action, title, content):
    if user.is_anonymous:
        user = None
    # ===---
    dmAdminLogs.objects.create(
        user=user,
        user_action=action,
        title=title,
        content=content
    )


# ========================================================================== #


@receiver(post_save, sender=ProductDefault)
@receiver(post_save, sender=ProductVariable)
def handle_product(sender, instance, created, raw, **kwargs):
    try:
        for entry in reversed(inspect.stack()):
            try:
                user = entry[0].f_locals["request"].user
                break
            except Exception:
                user = None
        if created:
            create_log(user, 1, instance._meta.verbose_name, instance.product_name)
        else:
            create_log(user, 2, instance._meta.verbose_name, instance.product_name)
    except Exception:
        pass

@receiver(post_delete, sender=ProductDefault)
@receiver(post_delete, sender=ProductVariable)
def handle_product_delete(sender, instance, **kwargs):
    for entry in reversed(inspect.stack()):
        try:
            user = entry[0].f_locals["request"].user
            break
        except Exception:
            user = None
    create_log(user, 3, instance._meta.verbose_name, instance.product_name)


@receiver(post_save, sender=ProductVariableVariant)
def handle_productvariant(sender, instance, created, raw, **kwargs):
    try:
        for entry in reversed(inspect.stack()):
            try:
                user = entry[0].f_locals["request"].user
                break
            except Exception:
                user = None
        content = instance.product.product_name+" "+instance.product_code
        if created:
            create_log(user, 1, instance._meta.verbose_name, content)
        else:
            create_log(user, 2, instance._meta.verbose_name, content)
    except Exception:
        pass


@receiver(post_delete, sender=ProductVariableVariant)
def handle_productvariant_delete(sender, instance, **kwargs):
    for entry in reversed(inspect.stack()):
        try:
            user = entry[0].f_locals["request"].user
            break
        except Exception:
            user = None
    content = instance.product.product_name+" "+instance.product_code
    create_log(user, 3, instance._meta.verbose_name, content)


@receiver(pre_save, sender=Order)
def handle_order_pre(sender, instance, raw, **kwargs):
    try:
        for entry in reversed(inspect.stack()):
            try:
                user = entry[0].f_locals["request"].user
                break
            except Exception:
                user = None
        old = Order.objects.filter(pk=instance.pk).first()
        if old is not None and old.status == "payment_confirmed" and old.status != instance.status:
            if instance.status == "ready_for_delivery":
                content = "#"+str(instance.get_number())+" : "+str(_("ready for delivery"))
            else:
                content = "#"+str(instance.get_number())
            create_log(user, 2, str(_("Order")), content)
    except Exception:
        pass


@receiver(post_save, sender=Order)
def handle_order_post(sender, instance, created, raw, **kwargs):
    try:
        if created:
            content = "#"+str(instance.get_number())
            create_log(instance.customer.user, 1, str(_("Order")), content)
    except Exception:
        pass


@receiver(post_save, sender=ProductCategory)
@receiver(post_save, sender=ProductBrand)
@receiver(post_save, sender=ProductLabel)
@receiver(post_save, sender=ProductFilterGroup)
@receiver(post_save, sender=ProductFilter)
@receiver(post_save, sender=dmRabaisPerCategory)
@receiver(post_save, sender=dmPromoCode)
def handle_modelwithname(sender, instance, created, raw, **kwargs):
    try:
        for entry in reversed(inspect.stack()):
            try:
                user = entry[0].f_locals["request"].user
                break
            except Exception:
                user = None
        if created:
            create_log(user, 1, instance._meta.verbose_name, instance.name)
        else:
            create_log(user, 2, instance._meta.verbose_name, instance.name)
    except Exception:
        pass


@receiver(post_delete, sender=ProductCategory)
@receiver(post_delete, sender=ProductBrand)
@receiver(post_delete, sender=ProductLabel)
@receiver(post_delete, sender=ProductFilterGroup)
@receiver(post_delete, sender=ProductFilter)
@receiver(post_delete, sender=dmRabaisPerCategory)
@receiver(post_delete, sender=dmPromoCode)
def handle_modelwithname_delete(sender, instance, **kwargs):
    for entry in reversed(inspect.stack()):
        try:
            user = entry[0].f_locals["request"].user
            break
        except Exception:
            user = None
    create_log(user, 3, instance._meta.verbose_name, instance.name)


@receiver(post_save, sender=dmAdvertisingTopBanner)
def handle_advertisingtopbanner(sender, instance, created, raw, **kwargs):
    try:
        for entry in reversed(inspect.stack()):
            try:
                user = entry[0].f_locals["request"].user
                break
            except Exception:
                user = None
        content = instance.text[0:32]+"..." if len(instance.text) > 32 else instance.text
        if created:
            create_log(user, 1, instance._meta.verbose_name, content)
        else:
            create_log(user, 2, instance._meta.verbose_name, content)
    except Exception:
        pass


@receiver(post_delete, sender=dmAdvertisingTopBanner)
def handle_advertisingtopbanner_delete(sender, instance, **kwargs):
    for entry in reversed(inspect.stack()):
        try:
            user = entry[0].f_locals["request"].user
            break
        except Exception:
            user = None
    content = instance.text[0:32]+"..." if len(instance.text) > 32 else instance.text
    create_log(user, 3, instance._meta.verbose_name, content)


@receiver(post_save, sender=dmAdvertisingPopup)
def handle_advertisingpopup(sender, instance, created, raw, **kwargs):
    try:
        for entry in reversed(inspect.stack()):
            try:
                user = entry[0].f_locals["request"].user
                break
            except Exception:
                user = None
        content = instance.title[0:32]+"..." if len(instance.title) > 32 else instance.title
        if created:
            create_log(user, 1, instance._meta.verbose_name, content)
        else:
            create_log(user, 2, instance._meta.verbose_name, content)
    except Exception:
        pass


@receiver(post_delete, sender=dmAdvertisingPopup)
def handle_advertisingpopup_delete(sender, instance, **kwargs):
    for entry in reversed(inspect.stack()):
        try:
            user = entry[0].f_locals["request"].user
            break
        except Exception:
            user = None
    content = instance.title[0:32]+"..." if len(instance.title) > 32 else instance.title
    create_log(user, 3, instance._meta.verbose_name, content)
