# Generated by Django 2.2.18 on 2021-02-24 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0055_auto_20210224_1110'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productfilter',
            options={'ordering': ['group', 'order', 'name'], 'verbose_name': "Product's Filter", 'verbose_name_plural': "Product's Filters"},
        ),
        migrations.AlterModelOptions(
            name='productfiltergroup',
            options={'ordering': ['order', 'name'], 'verbose_name': "Product's Filter Group", 'verbose_name_plural': "Product's Filter Groups"},
        ),
        migrations.AddField(
            model_name='productfiltergroup',
            name='order',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Sort by'),
        ),
    ]
