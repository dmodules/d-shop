# Generated by Django 2.2.18 on 2021-02-24 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0054_auto_20210224_1100'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productfiltergroup',
            options={'ordering': ['name'], 'verbose_name': "Product's Filter Group", 'verbose_name_plural': "Product's Filter Groups"},
        ),
    ]
