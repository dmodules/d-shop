# Generated by Django 2.2.18 on 2021-05-28 16:29

from django.db import migrations, models
import django.db.models.deletion
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0079_productfilter_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name_trans', models.CharField(max_length=250, verbose_name='Translated Attribute Name')),
                ('master', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='dshop.Attribute')),
            ],
            options={
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]