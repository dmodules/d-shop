# Generated by Django 2.2.17 on 2020-11-30 14:11

from django.db import migrations, models
import django.db.models.deletion
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('boutique', '0007_dmproductsbycategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='dmBlockSalesChild',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='boutique_dmblocksaleschild', serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Titre')),
                ('text', models.CharField(blank=True, max_length=100, null=True, verbose_name='Texte')),
                ('btn_label', models.CharField(blank=True, max_length=25, null=True, verbose_name="Button's Label")),
                ('btn_url', models.CharField(blank=True, max_length=255, null=True, verbose_name="Button's URL")),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='dmBlockSalesParent',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='boutique_dmblocksalesparent', serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Titre')),
                ('text', djangocms_text_ckeditor.fields.HTMLField(blank=True, null=True, verbose_name='Texte')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]