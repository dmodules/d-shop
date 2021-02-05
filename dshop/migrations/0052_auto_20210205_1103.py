# Generated by Django 2.2.17 on 2021-02-05 16:03

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0051_auto_20210205_0917'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Maximum 25 characters.', max_length=25, verbose_name="Label's Name")),
                ('colour', colorfield.fields.ColorField(default='#000', max_length=18, verbose_name="Label's Colour")),
            ],
            options={
                'verbose_name': "Product's Label",
                'verbose_name_plural': "Product's Labels",
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='label',
            field=models.ForeignKey(blank=True, help_text='Add a custom label to the product.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='dshop.ProductLabel', verbose_name='Label'),
        ),
    ]
