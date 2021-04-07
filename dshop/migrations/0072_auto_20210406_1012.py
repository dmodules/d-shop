# Generated by Django 2.2.18 on 2021-04-06 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0071_auto_20210329_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='dmsitecontact',
            name='map_latitude',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Map Latitude'),
        ),
        migrations.AddField(
            model_name='dmsitecontact',
            name='map_longitude',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Map Longitude'),
        ),
    ]