# Generated by Django 2.2.18 on 2021-03-23 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmRabais', '0016_dmpromocode_allow_multiple'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dmpromocode',
            name='allow_multiple',
            field=models.BooleanField(default=False, help_text='Allow customers to use this code multiple time?', verbose_name='Allow multiple uses?'),
        ),
        migrations.AlterField(
            model_name='dmpromocode',
            name='customer',
            field=models.ManyToManyField(blank=True, help_text='Only allow these customers to use this code. Leave blank to allow anyone.', limit_choices_to={'recognized': 2}, related_name='customerpromo', to='dshop.Customer', verbose_name='Customers'),
        ),
    ]
