# Generated by Django 2.2.17 on 2021-01-13 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0024_auto_20210113_0521'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='square_id',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Square ID'),
        ),
        migrations.AddField(
            model_name='attributevalue',
            name='square_id',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Square ID'),
        ),
    ]
