# Generated by Django 2.2.17 on 2021-01-11 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0018_auto_20210111_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dmblockcalltoaction',
            name='subtitle',
            field=models.CharField(blank=True, help_text='Maximum 250 characters.', max_length=250, null=True, verbose_name='Subtitle'),
        ),
        migrations.AlterField(
            model_name='dmblockcalltoaction',
            name='text',
            field=models.CharField(blank=True, help_text='Maximum 500 characters.', max_length=500, null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='dmblockcalltoaction',
            name='title',
            field=models.CharField(blank=True, help_text='Maximum 250 characters.', max_length=250, null=True, verbose_name='Title'),
        ),
    ]
