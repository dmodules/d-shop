# Generated by Django 2.2.17 on 2021-02-10 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmQuotation', '0004_auto_20210210_0852'),
    ]

    operations = [
        migrations.AddField(
            model_name='dmquotationitem',
            name='variant_attribute',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Variant Attribute'),
        ),
    ]
