# Generated by Django 2.2.18 on 2021-05-31 18:18

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('dmAdvertising', '0007_auto_20210531_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='dmadvertisingpopup',
            name='image_en',
            field=filer.fields.image.FilerImageField(blank=True, help_text='Recommended size: 800x600.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='advertisingpopup_image_en', to=settings.FILER_IMAGE_MODEL, verbose_name='Image EN'),
        ),
        migrations.AlterField(
            model_name='dmadvertisingpopup',
            name='image_fr',
            field=filer.fields.image.FilerImageField(help_text='Recommended size: 800x600.', on_delete=django.db.models.deletion.CASCADE, related_name='advertisingpopup_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Image FR'),
        ),
    ]