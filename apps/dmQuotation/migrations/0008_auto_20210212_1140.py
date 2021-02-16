# Generated by Django 2.2.17 on 2021-02-12 16:40

from django.db import migrations
import shop.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dmQuotation', '0007_dmquotationitem_product_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='dmquotation',
            name='extra',
            field=shop.models.fields.JSONField(verbose_name='Extra fields'),
        ),
        migrations.AddField(
            model_name='dmquotation',
            name='stored_request',
            field=shop.models.fields.JSONField(blank=True, null=True),
        ),
    ]