# Generated by Django 2.2.17 on 2021-02-09 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmSquare', '0002_auto_20210208_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dmstocklog',
            name='new_quantity',
            field=models.IntegerField(default=0, verbose_name='New Quantity'),
        ),
        migrations.AlterField(
            model_name='dmstocklog',
            name='old_quantity',
            field=models.IntegerField(default=0, verbose_name='Old Quantity'),
        ),
    ]
