# Generated by Django 2.2.18 on 2021-03-15 16:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='dmPortfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Maximum 250 characters.', max_length=250, verbose_name='Titre')),
                ('description', models.TextField(verbose_name="Description de l'emploi")),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.FILER_IMAGE_MODEL, verbose_name="Header's Image")),
            ],
            options={
                'verbose_name': 'Portefeuille',
                'verbose_name_plural': 'Portefeuilles',
            },
        ),
    ]
