# Generated by Django 2.2.17 on 2021-02-01 13:55

from django.db import migrations, models
import django.db.models.deletion
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0048_auto_20210128_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='dmSiteTermsAndConditions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', djangocms_text_ckeditor.fields.HTMLField(verbose_name='Text')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='termsandconditions', to='dshop.dmSite')),
            ],
            options={
                'verbose_name': 'Terms and Conditions',
                'verbose_name_plural': 'Terms and Conditions',
            },
        ),
    ]
