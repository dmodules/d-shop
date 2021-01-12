# Generated by Django 2.2.17 on 2021-01-12 09:22

from django.db import migrations
import shop.money.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0019_auto_20210111_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdefault',
            name='discounted_price',
            field=shop.money.fields.MoneyField(decimal_places=3, help_text='Net discounted price for this product.', null=True, verbose_name='Discounted Unit Price'),
        ),
    ]