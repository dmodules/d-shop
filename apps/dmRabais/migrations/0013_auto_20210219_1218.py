# Generated by Django 2.2.18 on 2021-02-19 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dmRabais', '0012_auto_20210219_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dmpromocode',
            name='discount_type',
        ),
        migrations.RemoveField(
            model_name='dmrabaispercategory',
            name='discount_type',
        ),
    ]
