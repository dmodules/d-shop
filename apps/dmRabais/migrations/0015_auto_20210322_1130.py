# Generated by Django 2.2.18 on 2021-03-22 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmRabais', '0014_auto_20210318_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dmpromocode',
            name='customer',
            field=models.ManyToManyField(blank=True, limit_choices_to={'recognized': 2}, related_name='customerpromo', to='dshop.Customer', verbose_name='Customers'),
        ),
    ]
