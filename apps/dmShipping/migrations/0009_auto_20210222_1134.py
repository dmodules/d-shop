# Generated by Django 2.2.18 on 2021-02-22 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmShipping', '0008_auto_20210219_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingallowed',
            name='cities',
            field=models.ManyToManyField(blank=True, to='dmShipping.ShippingCity', verbose_name='Cities'),
        ),
        migrations.AlterField(
            model_name='shippingallowed',
            name='countries',
            field=models.ManyToManyField(blank=True, to='dmShipping.ShippingCountry', verbose_name='Countries'),
        ),
        migrations.AlterField(
            model_name='shippingallowed',
            name='states',
            field=models.ManyToManyField(blank=True, to='dmShipping.ShippingState', verbose_name='States'),
        ),
        migrations.AlterField(
            model_name='shippingcity',
            name='code',
            field=models.CharField(help_text='Maximum 2 characters.', max_length=10, verbose_name='City Code'),
        ),
        migrations.AlterField(
            model_name='shippingstate',
            name='code',
            field=models.CharField(help_text='Maximum 2 characters.', max_length=10, verbose_name='State Code'),
        ),
    ]
