# Generated by Django 2.2.17 on 2021-01-19 12:45

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0034_categorytest'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productcategory',
            options={},
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='dshop.ProductCategory', verbose_name="Parent's Category"),
        ),
    ]
