# Generated by Django 2.2.18 on 2021-04-07 16:31

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('dshop', '0073_merge_20210406_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='dmsitelogo',
            name='favico_180',
            field=filer.fields.image.FilerImageField(blank=True, help_text='Size: 180x180. Format: .png', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='favico_180', to=settings.FILER_IMAGE_MODEL, verbose_name='Favicon 180x180'),
        ),
        migrations.AddField(
            model_name='dmsitelogo',
            name='favico_192',
            field=filer.fields.image.FilerImageField(blank=True, help_text='Size: 192x192. Format: .png', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='favico_192', to=settings.FILER_IMAGE_MODEL, verbose_name='Favicon 192x192'),
        ),
        migrations.AddField(
            model_name='dmsitelogo',
            name='favico_512',
            field=filer.fields.image.FilerImageField(blank=True, help_text='Size: 512x512. Format: .png', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='favico_512', to=settings.FILER_IMAGE_MODEL, verbose_name='Favicon 512x512'),
        ),
        migrations.AddField(
            model_name='dmsitelogo',
            name='favico_ico',
            field=filer.fields.image.FilerImageField(blank=True, help_text='Size: 48x48. Format: .ico', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='favico_ico', to=settings.FILER_IMAGE_MODEL, verbose_name='Favicon 48x48'),
        ),
    ]
