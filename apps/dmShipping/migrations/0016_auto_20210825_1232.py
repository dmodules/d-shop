# Generated by Django 2.2.18 on 2021-08-25 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmShipping', '0015_auto_20210825_1230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingmanagementtranslation',
            name='name_trans',
        ),
        migrations.AddField(
            model_name='shippingmanagementtranslation',
            name='name',
            field=models.CharField(default='Temporaire', max_length=255, verbose_name='Translated Attribute Name'),
            preserve_default=False,
        ),
    ]