# Generated by Django 2.2.18 on 2021-03-15 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0061_auto_20210312_0901'),
        ('dmRabais', '0011_dmpromocode_apply_on_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='dmpromocode',
            name='customer',
            field=models.ManyToManyField(related_name='customerpromo', to='dshop.Customer', verbose_name='Customers'),
        ),
    ]
