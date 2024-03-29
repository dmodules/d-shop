# Generated by Django 2.2.17 on 2021-01-12 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmShipping', '0003_auto_20210104_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingmanagement',
            name='identifier',
            field=models.CharField(choices=[('pickup-in-store', 'Pick Up in Store'), ('free-shipping', 'Postal shipping (free)'), ('standard-shipping', 'Postal shipping (standard)'), ('express-shipping', 'Postal shipping (express)'), ('standard-separator-shipping', 'Postal shipping with separator (standard)'), ('express-separator-shipping', 'Postal shipping with separator (express)')], default='free-shipping', max_length=100, unique=True, verbose_name='Identifier'),
        ),
    ]
