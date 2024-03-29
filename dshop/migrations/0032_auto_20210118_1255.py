# Generated by Django 2.2.17 on 2021-01-18 17:55

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0031_auto_20210115_1424'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productcategory',
            options={},
        ),
        migrations.AddField(
            model_name='productcategory',
            name='lft',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productcategory',
            name='mptt_level',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productcategory',
            name='rght',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productcategory',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='dshop.ProductCategory', verbose_name="Parent's Category"),
        ),
    ]
