# Generated by Django 2.2.17 on 2021-02-01 14:26

from django.db import migrations, models
import django.db.models.deletion
import djangocms_text_ckeditor.fields
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0049_dmsitetermsandconditions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dmsitetermsandconditions',
            name='text',
        ),
        migrations.CreateModel(
            name='dmSiteTermsAndConditionsTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('text', djangocms_text_ckeditor.fields.HTMLField(blank=True, null=True, verbose_name='Text')),
                ('master', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='dshop.dmSiteTermsAndConditions')),
            ],
            options={
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]