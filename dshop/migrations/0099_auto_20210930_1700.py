# Generated by Django 2.2.18 on 2021-09-30 17:00

import colorfield.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djangocms_text_ckeditor.fields
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('dshop', '0098_auto_20210826_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='dmTimelineParent',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='dshop_dmtimelineparent', serialize=False, to='cms.CMSPlugin')),
                ('hide_paddingtop', models.BooleanField(default=False, verbose_name='Hide Top Margin')),
                ('hide_paddingbot', models.BooleanField(default=False, verbose_name='Hide Bottom Margin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AddField(
            model_name='dmbloctext2column',
            name='hide_paddingbot',
            field=models.BooleanField(default=False, verbose_name='Hide Bottom Margin'),
        ),
        migrations.AddField(
            model_name='dmbloctext2column',
            name='hide_paddingtop',
            field=models.BooleanField(default=False, verbose_name='Hide Top Margin'),
        ),
        migrations.AddField(
            model_name='dmbloctextcarrousel',
            name='bg_color',
            field=colorfield.fields.ColorField(blank=True, default=None, help_text='Leave blank to use transparent.', max_length=18, null=True, verbose_name="Background's Colour"),
        ),
        migrations.AddField(
            model_name='dmbloctextcarrousel',
            name='btn_blank',
            field=models.BooleanField(default=False, verbose_name='Open on new tab?'),
        ),
        migrations.AddField(
            model_name='dmbloctextcarrousel',
            name='btn_label',
            field=models.CharField(blank=True, help_text='Facultative. Maximum 255 characters.', max_length=255, null=True, verbose_name="Link's Label"),
        ),
        migrations.AddField(
            model_name='dmbloctextcarrousel',
            name='btn_url',
            field=models.CharField(blank=True, help_text='Facultative. Maximum 1 000 characters.', max_length=1000, null=True, verbose_name='URL'),
        ),
        migrations.AddField(
            model_name='dmbloctextcarrousel',
            name='hide_paddingbot',
            field=models.BooleanField(default=False, verbose_name='Hide Bottom Margin'),
        ),
        migrations.AddField(
            model_name='dmbloctextcarrousel',
            name='hide_paddingtop',
            field=models.BooleanField(default=False, verbose_name='Hide Top Margin'),
        ),
        migrations.AddField(
            model_name='dmbloctextmedia',
            name='bg_color',
            field=colorfield.fields.ColorField(blank=True, default=None, help_text='Leave blank to use transparent.', max_length=18, null=True, verbose_name="Background's Colour"),
        ),
        migrations.AddField(
            model_name='dmbloctextmedia',
            name='btn_blank',
            field=models.BooleanField(default=False, verbose_name='Open on new tab?'),
        ),
        migrations.AddField(
            model_name='dmbloctextmedia',
            name='btn_label',
            field=models.CharField(blank=True, help_text='Facultative. Maximum 255 characters.', max_length=255, null=True, verbose_name="Link's Label"),
        ),
        migrations.AddField(
            model_name='dmbloctextmedia',
            name='btn_url',
            field=models.CharField(blank=True, help_text='Facultative. Maximum 1 000 characters.', max_length=1000, null=True, verbose_name='URL'),
        ),
        migrations.AddField(
            model_name='dmbloctextmedia',
            name='hide_paddingbot',
            field=models.BooleanField(default=False, verbose_name='Hide Bottom Margin'),
        ),
        migrations.AddField(
            model_name='dmbloctextmedia',
            name='hide_paddingtop',
            field=models.BooleanField(default=False, verbose_name='Hide Top Margin'),
        ),
        migrations.AddField(
            model_name='dmproductsbrands',
            name='bg_color',
            field=colorfield.fields.ColorField(blank=True, default=None, help_text='Leave blank to use transparent.', max_length=18, null=True, verbose_name="Background's Colour"),
        ),
        migrations.AlterField(
            model_name='dmblocksaleschild',
            name='text_position',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Left'), (1, 'Right'), (2, 'Center')], default=1, verbose_name="Text's Position"),
        ),
        migrations.CreateModel(
            name='dmTimelineChild',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='dshop_dmtimelinechild', serialize=False, to='cms.CMSPlugin')),
                ('timeline_label', models.CharField(blank=True, help_text='Maximum 8 characters. Will be displayed on the line of the middle.', max_length=8, null=True, verbose_name="Timeline's Label")),
                ('suptitle', models.CharField(blank=True, help_text='Maximum 255 characters.', max_length=255, null=True, verbose_name='Suptitle')),
                ('title', models.CharField(blank=True, help_text='Maximum 255 characters.', max_length=255, null=True, verbose_name='Title')),
                ('subtitle', models.CharField(blank=True, help_text='Maximum 255 characters.', max_length=255, null=True, verbose_name='Subtitle')),
                ('suptitle_color', colorfield.fields.ColorField(blank=True, default=None, max_length=18, null=True, verbose_name="Suptitle's Colour")),
                ('title_color', colorfield.fields.ColorField(blank=True, default=None, max_length=18, null=True, verbose_name="Title's Colour")),
                ('subtitle_color', colorfield.fields.ColorField(blank=True, default=None, max_length=18, null=True, verbose_name="Subtitle's Colour")),
                ('text', djangocms_text_ckeditor.fields.HTMLField(blank=True, null=True, verbose_name='Text')),
                ('position_text', models.PositiveSmallIntegerField(choices=[(1, 'Left'), (2, 'Right')], default=1, verbose_name="Text's Position")),
                ('image', filer.fields.image.FilerImageField(blank=True, help_text='Maximum size: 800x800. Leave blank to hide image.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dmplugin_timeline_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='dmTilesParent',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='dshop_dmtilesparent', serialize=False, to='cms.CMSPlugin')),
                ('fullwide', models.BooleanField(default=True, verbose_name='Fullwide')),
                ('bg_color', colorfield.fields.ColorField(blank=True, default=None, max_length=18, null=True, verbose_name="Background's Colour")),
                ('perline', models.CharField(choices=[('12', '1'), ('6', '2'), ('4', '3'), ('3', '4')], default='6', max_length=2, verbose_name='Tile Per Line')),
                ('hide_paddingtop', models.BooleanField(default=False, verbose_name='Hide Top Margin')),
                ('hide_paddingbot', models.BooleanField(default=False, verbose_name='Hide Bottom Margin')),
                ('bg_image', filer.fields.image.FilerImageField(blank=True, help_text='Facultative. Size: 2000x900.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dmplugin_tilesparent_bgimage', to=settings.FILER_IMAGE_MODEL, verbose_name="Background's Image")),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='dmTilesChild',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='dshop_dmtileschild', serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Title')),
                ('label', models.CharField(blank=True, default='Voir', help_text='Facultative.', max_length=1000, null=True, verbose_name='Label')),
                ('link', models.CharField(blank=True, help_text='Facultative.', max_length=1000, null=True, verbose_name='URL')),
                ('blank', models.BooleanField(default=False, verbose_name='Open on new tab?')),
                ('text_color', colorfield.fields.ColorField(default='#000000', max_length=18, verbose_name="Text's Colour")),
                ('image', filer.fields.image.FilerImageField(blank=True, help_text='Facultative. Max size: 1000x1000.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dmplugin_tileschild_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]