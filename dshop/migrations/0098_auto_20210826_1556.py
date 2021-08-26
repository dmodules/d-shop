# Generated by Django 2.2.18 on 2021-08-26 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0097_auto_20210825_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attributetranslation',
            name='name_trans',
            field=models.CharField(help_text='Maximum 255 characters.', max_length=255, verbose_name='Displayed Text'),
        ),
        migrations.AlterField(
            model_name='attributevaluetranslation',
            name='value_trans',
            field=models.CharField(help_text='Maximum 255 characters.', max_length=255, verbose_name='Displayed Text'),
        ),
    ]
