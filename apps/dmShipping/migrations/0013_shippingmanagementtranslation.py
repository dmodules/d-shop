# Generated by Django 2.2.18 on 2021-05-31 18:37

from django.db import migrations, models
import django.db.models.deletion
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('dmShipping', '0012_merge_20210401_0948'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingManagementTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name_trans', models.CharField(max_length=255, verbose_name='Translated Attribute Name')),
                ('master', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='dmShipping.ShippingManagement')),
            ],
            options={
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]