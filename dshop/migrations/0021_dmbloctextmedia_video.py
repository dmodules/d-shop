# Generated by Django 2.2.17 on 2021-01-12 18:54

from django.db import migrations
import django.db.models.deletion
import filer.fields.file


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0012_file_mime_type'),
        ('dshop', '0020_auto_20210112_0422'),
    ]

    operations = [
        migrations.AddField(
            model_name='dmbloctextmedia',
            name='video',
            field=filer.fields.file.FilerFileField(blank=True, help_text='Leave blank to hide or use image instead.', null=True, on_delete=django.db.models.deletion.CASCADE, to='filer.File', verbose_name='Video'),
        ),
    ]
