# Generated by Django 2.2.18 on 2021-02-23 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmShipping', '0010_auto_20210222_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingallowed',
            name='cities',
            field=models.ManyToManyField(blank=True, to='cities_light.City', verbose_name='Cities'),
        ),
        migrations.AlterField(
            model_name='shippingallowed',
            name='countries',
            field=models.ManyToManyField(blank=True, to='cities_light.Country', verbose_name='Countries'),
        ),
        migrations.AlterField(
            model_name='shippingallowed',
            name='states',
            field=models.ManyToManyField(blank=True, to='cities_light.Region', verbose_name='States'),
        ),
    ]
