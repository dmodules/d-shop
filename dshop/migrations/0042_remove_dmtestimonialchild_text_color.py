# Generated by Django 2.2.17 on 2021-01-26 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0041_auto_20210126_1444'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dmtestimonialchild',
            name='text_color',
        ),
    ]