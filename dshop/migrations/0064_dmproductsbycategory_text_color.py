# Generated by Django 2.2.18 on 2021-03-18 18:57

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0063_dmblocsliderparent_height'),
    ]

    operations = [
        migrations.AddField(
            model_name='dmproductsbycategory',
            name='text_color',
            field=colorfield.fields.ColorField(blank=True, default=None, max_length=18, null=True, verbose_name="Text's Colour"),
        ),
    ]