# Generated by Django 2.2.18 on 2021-03-15 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0061_auto_20210312_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='dmsitecontact',
            name='schedule',
            field=models.TextField(blank=True, null=True, verbose_name='Schedule'),
        ),
    ]
