# Generated by Django 2.2.18 on 2021-03-24 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0067_auto_20210324_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='dmbloctextcarrousel',
            name='crop_image',
            field=models.BooleanField(default=True, help_text='If checked, will crop images to fit the same ratio.', verbose_name='Crop Image?'),
        ),
    ]