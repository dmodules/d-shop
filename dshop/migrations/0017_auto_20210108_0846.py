# Generated by Django 2.2.17 on 2021-01-08 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0016_merge_20210108_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdefault',
            name='end_date',
            field=models.DateTimeField(blank=True, help_text='Stop DateTime Discount', null=True, verbose_name='Discount Stop DateTime'),
        ),
    ]
