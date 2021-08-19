# Generated by Django 2.2.18 on 2021-08-19 14:47

import colorfield.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djangocms_text_ckeditor.fields
import filer.fields.file
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0093_auto_20210804_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='dmtestimonialchild',
            name='job',
            field=models.CharField(blank=True, help_text='Maximum 255 characters.', max_length=255, null=True, verbose_name='Job'),
        ),
        migrations.AddField(
            model_name='dmtestimonialchild',
            name='job_color',
            field=colorfield.fields.ColorField(default='#292b2c', max_length=18, verbose_name="Job's Colour"),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='name',
            field=models.CharField(help_text='Maximum 255 characters.', max_length=255, verbose_name='Attribute Name'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='square_id',
            field=models.CharField(blank=True, help_text='Facultative. Maximum 30 characters.', max_length=30, null=True, verbose_name='Square ID'),
        ),
        migrations.AlterField(
            model_name='attributetranslation',
            name='name_trans',
            field=models.CharField(help_text='Maximum 255 characters.', max_length=255, verbose_name='Translated Attribute Name'),
        ),
        migrations.AlterField(
            model_name='attributevalue',
            name='square_id',
            field=models.CharField(blank=True, help_text='Facultative. Maximum 30 characters.', max_length=30, null=True, verbose_name='Square ID'),
        ),
        migrations.AlterField(
            model_name='attributevalue',
            name='value',
            field=models.CharField(help_text='Maximum 255 characters.', max_length=255, verbose_name='Attribute Value'),
        ),
        migrations.AlterField(
            model_name='attributevaluetranslation',
            name='value_trans',
            field=models.CharField(help_text='Maximum 255 characters.', max_length=255, verbose_name='Translated Attribute Name'),
        ),
        migrations.AlterField(
            model_name='dmblocentetevideo',
            name='videofile',
            field=filer.fields.file.FilerFileField(help_text='Prioritize .mp4 format.', on_delete=django.db.models.deletion.CASCADE, to='filer.File', verbose_name='Video File'),
        ),
        migrations.AlterField(
            model_name='dmblocetapeschild',
            name='image',
            field=filer.fields.image.FilerImageField(blank=True, help_text='Facultative. Size: 160x160.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dmplugin_etapeschild_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='dmblockcalltoaction',
            name='image',
            field=filer.fields.image.FilerImageField(blank=True, help_text='Facultative. Size: 420x460.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dmplugin_calltoaction_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='dmblocksaleschild',
            name='image',
            field=filer.fields.image.FilerImageField(blank=True, help_text='Facultative. Size: 540x300.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dmplugin_saleschild_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='dmblocsliderchild',
            name='btn_label',
            field=models.CharField(blank=True, help_text='Facultative. Maximum 255 characters.', max_length=255, null=True, verbose_name="Link's Label"),
        ),
        migrations.AlterField(
            model_name='dmblocsliderchild',
            name='btn_url',
            field=models.CharField(blank=True, help_text='Facultative. Maximum 1 000 characters.', max_length=1000, null=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='dmblocsliderchild',
            name='image',
            field=filer.fields.image.FilerImageField(blank=True, help_text='Maximum size: 1920x900. Leave blank to hide image.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dmplugin_sliderchild_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='dmblocsliderchild',
            name='subtitle',
            field=models.CharField(blank=True, help_text='Maximum 255 characters.', max_length=255, null=True, verbose_name='Subtitle'),
        ),
        migrations.AlterField(
            model_name='dmblocsliderchild',
            name='suptitle',
            field=models.CharField(blank=True, help_text='Maximum 255 characters.', max_length=255, null=True, verbose_name='Suptitle'),
        ),
        migrations.AlterField(
            model_name='dmblocsliderchild',
            name='title',
            field=models.CharField(blank=True, help_text='Maximum 255 characters.', max_length=255, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dmbloctext2column',
            name='subtitle',
            field=models.CharField(blank=True, help_text='Maximum 255 characters.', max_length=255, null=True, verbose_name='Subtitle'),
        ),
        migrations.AlterField(
            model_name='dmbloctext2column',
            name='title',
            field=models.CharField(blank=True, help_text='Maximum 255 characters.', max_length=255, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dmbloctextcarrousel',
            name='subtitle',
            field=models.CharField(blank=True, help_text='Maximum 255 characters.', max_length=255, null=True, verbose_name='Subtitle'),
        ),
        migrations.AlterField(
            model_name='dmbloctextcarrousel',
            name='title',
            field=models.CharField(blank=True, help_text='Maximum 255 characters.', max_length=255, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dmbloctextcarrouselimage',
            name='image',
            field=filer.fields.image.FilerImageField(help_text='Max sizes : 600x600. Always             use the same ratio on the same carrousel.', on_delete=django.db.models.deletion.CASCADE, related_name='dmplugin_textcarrousel_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='dmbloctextmedia',
            name='image',
            field=filer.fields.image.FilerImageField(blank=True, help_text='Sizes : 398x531. Leave blank to hide image.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dmplugin_textmedia_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='dmbloctextmedia',
            name='subtitle',
            field=models.CharField(blank=True, help_text='Maximum 255 characters.', max_length=255, null=True, verbose_name='Subtitle'),
        ),
        migrations.AlterField(
            model_name='dmbloctextmedia',
            name='title',
            field=models.CharField(blank=True, help_text='Maximum 255 characters.', max_length=255, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dmbloctextmedia',
            name='video',
            field=filer.fields.file.FilerFileField(blank=True, help_text='Leave blank to hide or use image instead.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dmplugin_textmedia_video', to='filer.File', verbose_name='Video'),
        ),
        migrations.AlterField(
            model_name='dminfolettre',
            name='image',
            field=filer.fields.image.FilerImageField(blank=True, help_text='Facultative. Size: 2000x900. Leave blank to hide image.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dmplugin_infolettre_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='dmproductsbrands',
            name='title',
            field=models.CharField(blank=True, help_text='Maximum 255 characters.', max_length=255, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dmproductsbycategory',
            name='bg_image',
            field=filer.fields.image.FilerImageField(blank=True, help_text='Facultative. Size: 2000x900.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bg_image', to=settings.FILER_IMAGE_MODEL, verbose_name="Background's Image"),
        ),
        migrations.AlterField(
            model_name='dmproductsbycategory',
            name='text',
            field=djangocms_text_ckeditor.fields.HTMLField(blank=True, help_text='Facultative.', null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='dmproductsbycategory',
            name='title',
            field=models.CharField(blank=True, help_text='Facultative. Maximum 255 characters.', max_length=255, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dmproductscategories',
            name='label',
            field=models.CharField(blank=True, default='See all', help_text='Facultative.             Maximum 255 characters.                  Leave blank to hide button.', max_length=255, null=True, verbose_name="Button's Label"),
        ),
        migrations.AlterField(
            model_name='dmproductscategories',
            name='title',
            field=models.CharField(blank=True, help_text='Maximum 255 characters.', max_length=255, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dmproductsvedette',
            name='text',
            field=djangocms_text_ckeditor.fields.HTMLField(blank=True, help_text='Facultative.', null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='dmproductsvedette',
            name='title',
            field=models.CharField(blank=True, help_text='Facultative. Maximum 255 characters.', max_length=255, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dmsitecontact',
            name='phone_secondary',
            field=models.CharField(blank=True, help_text='Facultative.', max_length=20, null=True, verbose_name='Secondary Phone'),
        ),
        migrations.AlterField(
            model_name='dmtestimonialchild',
            name='photo',
            field=filer.fields.image.FilerImageField(blank=True, help_text='Facultative. Size: 120x120.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dmplugin_testimonialchild_photo', to=settings.FILER_IMAGE_MODEL, verbose_name='Photo'),
        ),
        migrations.AlterField(
            model_name='dmtestimonialparent',
            name='bg_image',
            field=filer.fields.image.FilerImageField(blank=True, help_text='Facultative. Size: 2000x900.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dmplugin_testimonialparent_bgimage', to=settings.FILER_IMAGE_MODEL, verbose_name="Background's Image"),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(help_text='Maximum 255 characters.', max_length=255, verbose_name="Product's Name"),
        ),
        migrations.AlterField(
            model_name='productbrand',
            name='logo',
            field=filer.fields.image.FilerImageField(help_text='Size: 300x300.', on_delete=django.db.models.deletion.CASCADE, related_name='brand_logo', to=settings.FILER_IMAGE_MODEL, verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='productbrand',
            name='name',
            field=models.CharField(help_text='Maximum 255 characters.', max_length=255, verbose_name="Brand's Name"),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='image',
            field=filer.fields.image.FilerImageField(blank=True, help_text='Size: 2000x900.                 An image that will be shown on the top of the page of                      the Products of this category.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_image', to=settings.FILER_IMAGE_MODEL, verbose_name="Header's Image"),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='name',
            field=models.CharField(help_text='Maximum 255 characters.', max_length=255, verbose_name="Category's Name"),
        ),
        migrations.AlterField(
            model_name='productcategorytranslation',
            name='name_trans',
            field=models.CharField(help_text='Maximum 255 characters.', max_length=255, verbose_name='Translated Category Name'),
        ),
        migrations.AlterField(
            model_name='productdefault',
            name='product_code',
            field=models.CharField(help_text='A unique code.             Maximum 255 characters.                  Prioritize creating a new product instead of                       updating this code.', max_length=255, unique=True, verbose_name="Product's Code"),
        ),
        migrations.AlterField(
            model_name='productdocument',
            name='name',
            field=models.CharField(help_text='Maximum 255 characters.', max_length=255, verbose_name="Document's Name"),
        ),
        migrations.AlterField(
            model_name='productfilter',
            name='image',
            field=filer.fields.image.FilerImageField(blank=True, help_text='Size: 2000x900.             An image that will be shown on the top of the page of                  the Products of this filter.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='filter_image', to=settings.FILER_IMAGE_MODEL, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='productfilter',
            name='name',
            field=models.CharField(help_text='Maximum 255 characters.', max_length=255, verbose_name="Filter's Name"),
        ),
        migrations.AlterField(
            model_name='productfiltergroup',
            name='name',
            field=models.CharField(help_text='Maximum 255 characters.', max_length=255, verbose_name="Filter's Group Name"),
        ),
        migrations.AlterField(
            model_name='productfiltergrouptranslation',
            name='name_trans',
            field=models.CharField(blank=True, help_text='Maximum 255 characters.', max_length=255, null=True, verbose_name="Translated Filter's Group Name"),
        ),
        migrations.AlterField(
            model_name='productfiltertranslation',
            name='name_trans',
            field=models.CharField(blank=True, help_text='Maximum 255 characters.', max_length=255, null=True, verbose_name="Translated Filter's Name"),
        ),
        migrations.AlterField(
            model_name='producttranslation',
            name='product_name_trans',
            field=models.CharField(help_text='Maximum 255 characters.', max_length=255, null=True, verbose_name="Product's Name"),
        ),
        migrations.AlterField(
            model_name='productvariable',
            name='square_id',
            field=models.CharField(blank=True, help_text='Facultative. Maximum 30 characters.', max_length=30, null=True, verbose_name='Square ID'),
        ),
        migrations.AlterField(
            model_name='productvariablevariant',
            name='product_code',
            field=models.CharField(help_text='A unique code.             Maximum 255 characters.                  Prioritize creating a new product instead of                       updating this code.', max_length=255, unique=True, verbose_name="Product's Code"),
        ),
        migrations.AlterField(
            model_name='productvariablevariant',
            name='variant_image',
            field=filer.fields.image.FilerImageField(blank=True, help_text='Recommended size: 810x900.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='variant_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Variant Image'),
        ),
    ]
