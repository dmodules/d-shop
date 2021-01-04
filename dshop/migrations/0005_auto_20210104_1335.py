# Generated by Django 2.2.17 on 2021-01-04 18:35

import colorfield.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import djangocms_text_ckeditor.fields
import filer.fields.file
import filer.fields.image
import shop.models.fields
import shop.money.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0004_auto_20201221_0657'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dmsitesocial',
            options={'verbose_name': 'Social Network', 'verbose_name_plural': 'Social Networks'},
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={'ordering': ['order', 'parent__name', 'name'], 'verbose_name': "Product's Category", 'verbose_name_plural': "Product's Categories"},
        ),
        migrations.AlterModelOptions(
            name='productdefault',
            options={'verbose_name': 'Default Product', 'verbose_name_plural': 'Default Products'},
        ),
        migrations.AlterModelOptions(
            name='productdefaulttranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'Default Product Translation'},
        ),
        migrations.AlterModelOptions(
            name='productfilter',
            options={'ordering': ['order', 'name'], 'verbose_name': "Product's Filter", 'verbose_name_plural': "Product's Filters"},
        ),
        migrations.AlterModelOptions(
            name='productvariable',
            options={'verbose_name': 'Variable Product', 'verbose_name_plural': 'Variable Products'},
        ),
        migrations.AlterModelOptions(
            name='productvariabletranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'Variable Product Translation'},
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='address1',
            field=models.CharField(max_length=1024, verbose_name='Address 1'),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='address2',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Address 2'),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='city',
            field=models.CharField(max_length=1024, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='country',
            field=models.CharField(max_length=4, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='name',
            field=models.CharField(max_length=1024, verbose_name='Fullname'),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='province',
            field=models.CharField(max_length=1024, verbose_name='Province / State'),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='zip_code',
            field=models.CharField(max_length=255, verbose_name='Postal Code'),
        ),
        migrations.AlterField(
            model_name='dmbloccontact',
            name='horaire_bot',
            field=models.CharField(help_text='Maximum 50 characters.', max_length=50, verbose_name='Schedule - Bottom'),
        ),
        migrations.AlterField(
            model_name='dmbloccontact',
            name='horaire_top',
            field=models.CharField(help_text='Maximum 50 characters.', max_length=50, verbose_name='Schedule - Top'),
        ),
        migrations.AlterField(
            model_name='dmbloccontact',
            name='link_label',
            field=models.CharField(default='Contact Us', help_text='Maximum 50 characters.', max_length=50, verbose_name="Button's Label"),
        ),
        migrations.AlterField(
            model_name='dmbloccontact',
            name='phone_bot',
            field=models.CharField(default='Call Us', help_text='Maximum 50 characters.', max_length=50, verbose_name='Phone - Bottom'),
        ),
        migrations.AlterField(
            model_name='dmbloccontact',
            name='phone_top',
            field=models.CharField(help_text='Maximum 50 characters.', max_length=50, verbose_name='Phone - Top'),
        ),
        migrations.AlterField(
            model_name='dmbloccontact',
            name='where_bot',
            field=models.CharField(default='Our Address', help_text='Maximum 50 characters.', max_length=50, verbose_name='Address - Bottom'),
        ),
        migrations.AlterField(
            model_name='dmbloccontact',
            name='where_top',
            field=models.CharField(help_text='Maximum 120 characters.', max_length=120, verbose_name='Address - Top'),
        ),
        migrations.AlterField(
            model_name='dmblocentete',
            name='title',
            field=models.CharField(blank=True, help_text='Maximum 255 characters.', max_length=255, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dmblocentetevideo',
            name='videofile',
            field=filer.fields.file.FilerFileField(on_delete=django.db.models.deletion.CASCADE, to='filer.File', verbose_name='Video File'),
        ),
        migrations.AlterField(
            model_name='dmblocetapeschild',
            name='image',
            field=models.ImageField(blank=True, help_text='Sizes : 160x160.', null=True, upload_to='', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='dmblocetapeschild',
            name='text',
            field=models.CharField(blank=True, help_text='Maximum 200 characters.', max_length=200, null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='dmblocetapeschild',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dmblocetapesparent',
            name='subtitle',
            field=models.CharField(blank=True, help_text='Maximum 200 characters.', max_length=200, null=True, verbose_name='Subtitle'),
        ),
        migrations.AlterField(
            model_name='dmblocetapesparent',
            name='title',
            field=models.CharField(blank=True, help_text='Maximum 100 characters.', max_length=100, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dmblockcalltoaction',
            name='bg_color',
            field=colorfield.fields.ColorField(blank=True, default=None, max_length=18, null=True, verbose_name="Background's Colour"),
        ),
        migrations.AlterField(
            model_name='dmblockcalltoaction',
            name='btn_label',
            field=models.CharField(blank=True, help_text='Maximum 25 characters.', max_length=25, null=True, verbose_name="Button's Label"),
        ),
        migrations.AlterField(
            model_name='dmblockcalltoaction',
            name='btn_url',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name="Button's URL"),
        ),
        migrations.AlterField(
            model_name='dmblockcalltoaction',
            name='subtitle',
            field=models.CharField(blank=True, help_text='Maximum 100 characters.', max_length=100, null=True, verbose_name='Subtitle'),
        ),
        migrations.AlterField(
            model_name='dmblockcalltoaction',
            name='subtitle_color',
            field=colorfield.fields.ColorField(default='#292b2c', max_length=18, verbose_name="Subtitle's Colour"),
        ),
        migrations.AlterField(
            model_name='dmblockcalltoaction',
            name='text',
            field=models.CharField(blank=True, help_text='Maximum 100 characters.', max_length=100, null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='dmblockcalltoaction',
            name='text_color',
            field=colorfield.fields.ColorField(default='#292b2c', max_length=18, verbose_name="Text's Colour"),
        ),
        migrations.AlterField(
            model_name='dmblockcalltoaction',
            name='title',
            field=models.CharField(blank=True, help_text='Maximum 100 characters.', max_length=100, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dmblockcalltoaction',
            name='title_color',
            field=colorfield.fields.ColorField(default='#292b2c', max_length=18, verbose_name="Title's Colour"),
        ),
        migrations.AlterField(
            model_name='dmblocksaleschild',
            name='bg_color',
            field=colorfield.fields.ColorField(default='#f2f2f3', max_length=18, verbose_name="Background's Colour"),
        ),
        migrations.AlterField(
            model_name='dmblocksaleschild',
            name='btn_label',
            field=models.CharField(blank=True, help_text='Maximum 25 characters.', max_length=25, null=True, verbose_name="Button's Label"),
        ),
        migrations.AlterField(
            model_name='dmblocksaleschild',
            name='btn_url',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name="Button's URL"),
        ),
        migrations.AlterField(
            model_name='dmblocksaleschild',
            name='text',
            field=models.CharField(blank=True, help_text='Maximum 100 characters.', max_length=100, null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='dmblocksaleschild',
            name='title',
            field=models.CharField(blank=True, help_text='Maximum 100 characters.', max_length=100, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dmblocksaleschild',
            name='txt_color',
            field=colorfield.fields.ColorField(default='#292b2c', max_length=18, verbose_name="Text's Colour"),
        ),
        migrations.AlterField(
            model_name='dmblocksalesparent',
            name='text',
            field=djangocms_text_ckeditor.fields.HTMLField(blank=True, null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='dmblocksalesparent',
            name='title',
            field=models.CharField(blank=True, help_text='Maximum 100 characters.', max_length=100, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dmblocsliderchild',
            name='bg_color',
            field=colorfield.fields.ColorField(blank=True, default=None, max_length=18, null=True, verbose_name="Background's Colour"),
        ),
        migrations.AlterField(
            model_name='dmblocsliderchild',
            name='btn_blank',
            field=models.BooleanField(default=False, verbose_name='Open on new tab?'),
        ),
        migrations.AlterField(
            model_name='dmblocsliderchild',
            name='btn_label',
            field=models.CharField(blank=True, help_text='Maximum 30 characters.', max_length=30, null=True, verbose_name="Link's Label"),
        ),
        migrations.AlterField(
            model_name='dmblocsliderchild',
            name='btn_url',
            field=models.CharField(blank=True, help_text='Maximum 1 000 characters.', max_length=1000, null=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='dmblocsliderchild',
            name='image',
            field=models.ImageField(blank=True, help_text='Leave blank to hide image.', null=True, upload_to='', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='dmblocsliderchild',
            name='position_text',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Left'), (2, 'Middle'), (3, 'Right')], default=3, verbose_name="Text's Position"),
        ),
        migrations.AlterField(
            model_name='dmblocsliderchild',
            name='subtitle',
            field=models.CharField(blank=True, help_text='Maximum 200 characters.', max_length=200, null=True, verbose_name='Subtitle'),
        ),
        migrations.AlterField(
            model_name='dmblocsliderchild',
            name='subtitle_color',
            field=colorfield.fields.ColorField(blank=True, default=None, max_length=18, null=True, verbose_name="Subtitle's Colour"),
        ),
        migrations.AlterField(
            model_name='dmblocsliderchild',
            name='title',
            field=models.CharField(blank=True, help_text='Maximum 100 characters.', max_length=100, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dmblocsliderchild',
            name='title_color',
            field=colorfield.fields.ColorField(blank=True, default=None, max_length=18, null=True, verbose_name="Title's Colour"),
        ),
        migrations.AlterField(
            model_name='dmbloctextmedia',
            name='colposition',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Left'), (1, 'Right')], default=1, verbose_name="Image's Position"),
        ),
        migrations.AlterField(
            model_name='dmbloctextmedia',
            name='image',
            field=models.ImageField(blank=True, help_text='Sizes : 398x531. Leave blank to hide image.', null=True, upload_to='', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='dmbloctextmedia',
            name='subtitle',
            field=models.CharField(blank=True, help_text='Maximum 200 characters.', max_length=200, null=True, verbose_name='Subtitle'),
        ),
        migrations.AlterField(
            model_name='dmbloctextmedia',
            name='text',
            field=djangocms_text_ckeditor.fields.HTMLField(blank=True, null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='dmbloctextmedia',
            name='title',
            field=models.CharField(blank=True, help_text='Maximum 100 characters.', max_length=100, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dminfolettre',
            name='image',
            field=models.ImageField(blank=True, help_text='Leave blank to hide image.', null=True, upload_to='', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='dminfolettre',
            name='label',
            field=models.CharField(default='Subscribe to our newsletter', help_text='Maximum 200 characters.', max_length=200, verbose_name="Button's Label"),
        ),
        migrations.AlterField(
            model_name='dminfolettre',
            name='subtitle',
            field=models.CharField(blank=True, help_text='Maximum 200 characters.', max_length=200, null=True, verbose_name='Subtitle'),
        ),
        migrations.AlterField(
            model_name='dminfolettre',
            name='text',
            field=djangocms_text_ckeditor.fields.HTMLField(blank=True, null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='dminfolettre',
            name='title',
            field=models.CharField(blank=True, help_text='Maximum 100 characters.', max_length=100, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dmproductsbycategory',
            name='text',
            field=djangocms_text_ckeditor.fields.HTMLField(blank=True, null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='dmproductsbycategory',
            name='title',
            field=models.CharField(blank=True, help_text='Maximum 100 characters.', max_length=100, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dmproductscategories',
            name='label',
            field=models.CharField(blank=True, default='See all', help_text='Leave blank to hide button.', max_length=200, null=True, verbose_name="Button's Label"),
        ),
        migrations.AlterField(
            model_name='dmproductscategories',
            name='text',
            field=djangocms_text_ckeditor.fields.HTMLField(blank=True, null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='dmproductscategories',
            name='title',
            field=models.CharField(blank=True, help_text='Maximum 100 characters.', max_length=100, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dmproductsvedette',
            name='text',
            field=djangocms_text_ckeditor.fields.HTMLField(blank=True, null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='dmproductsvedette',
            name='title',
            field=models.CharField(blank=True, help_text='Maximum 100 characters.', max_length=100, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='dmsitecontact',
            name='address',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='dmsitecontact',
            name='email',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='dmsitecontact',
            name='phone',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='dmsitesocial',
            name='social',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Facebook'), (2, 'Instagram'), (3, 'Youtube'), (4, 'Twitter')], default=1, verbose_name='Social Network'),
        ),
        migrations.AlterField(
            model_name='dmsitesocial',
            name='url',
            field=models.CharField(max_length=1000, verbose_name='Link'),
        ),
        migrations.AlterField(
            model_name='featurelist',
            name='is_enabled',
            field=models.BooleanField(default=False, verbose_name='Is enabled?'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(verbose_name='Ordered Quantity'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='variables',
            field=shop.models.fields.JSONField(verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, to='dshop.ProductCategory', verbose_name='Categories'),
        ),
        migrations.AlterField(
            model_name='product',
            name='filters',
            field=models.ManyToManyField(blank=True, to='dshop.ProductFilter', verbose_name='Filters'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_vedette',
            field=models.BooleanField(default=False, verbose_name='Featured'),
        ),
        migrations.AlterField(
            model_name='product',
            name='main_image',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Main Image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(max_length=255, verbose_name="Product's Name"),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='name',
            field=models.CharField(max_length=100, verbose_name="Category's Name"),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='order',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Sort by'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dshop.ProductCategory', verbose_name="Parent's Category"),
        ),
        migrations.AlterField(
            model_name='productdefault',
            name='product_code',
            field=models.CharField(help_text='A unique code.', max_length=255, unique=True, verbose_name="Product's Code"),
        ),
        migrations.AlterField(
            model_name='productdefault',
            name='quantity',
            field=models.PositiveIntegerField(default=0, help_text='Available quantity in stock.', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Quantity'),
        ),
        migrations.AlterField(
            model_name='productdefault',
            name='unit_price',
            field=shop.money.fields.MoneyField(decimal_places=3, help_text='Net price for this product.', verbose_name='Unit Price'),
        ),
        migrations.AlterField(
            model_name='productdefaulttranslation',
            name='description',
            field=djangocms_text_ckeditor.fields.HTMLField(help_text='Long description.', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='productfilter',
            name='name',
            field=models.CharField(max_length=100, verbose_name="Filter's Name"),
        ),
        migrations.AlterField(
            model_name='productfilter',
            name='order',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Sort by'),
        ),
        migrations.AlterField(
            model_name='producttranslation',
            name='caption',
            field=djangocms_text_ckeditor.fields.HTMLField(blank=True, help_text='Short description.', null=True, verbose_name='Caption'),
        ),
        migrations.AlterField(
            model_name='producttranslation',
            name='description',
            field=djangocms_text_ckeditor.fields.HTMLField(blank=True, help_text='Long description.', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='productvariabletranslation',
            name='description',
            field=djangocms_text_ckeditor.fields.HTMLField(help_text='Long description.', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='productvariablevariant',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='dshop.ProductVariable', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='productvariablevariant',
            name='product_code',
            field=models.CharField(max_length=255, unique=True, verbose_name="Product's Code"),
        ),
        migrations.AlterField(
            model_name='productvariablevariant',
            name='quantity',
            field=models.PositiveIntegerField(default=0, help_text='Available quantity in stock.', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Quantity'),
        ),
        migrations.AlterField(
            model_name='productvariablevariant',
            name='unit_price',
            field=shop.money.fields.MoneyField(decimal_places=3, help_text='Net price for this product.', verbose_name='Unit Price'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='address1',
            field=models.CharField(max_length=1024, verbose_name='Address 1'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='address2',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Address 2'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='city',
            field=models.CharField(max_length=1024, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='country',
            field=models.CharField(max_length=4, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='name',
            field=models.CharField(max_length=1024, verbose_name='Fullname'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='province',
            field=models.CharField(max_length=1024, verbose_name='Province / State'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='zip_code',
            field=models.CharField(max_length=255, verbose_name='Postal Code'),
        ),
    ]
