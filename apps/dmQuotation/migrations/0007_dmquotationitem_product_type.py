# Generated by Django 2.2.17 on 2021-02-11 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmQuotation', '0006_merge_20210210_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='dmquotationitem',
            name='product_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Default'), (2, 'Variable')], default=1, verbose_name='Product Type'),
        ),
    ]
