# Generated by Django 2.2.17 on 2020-12-09 12:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='dmRabaisPerCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('amount', models.DecimalField(blank=True, decimal_places=3, help_text='Un montant fixe à retirer du prix original, laisser vide pour privilégier le pourcentage.', max_digits=30, null=True, verbose_name='Montant fixe')),
                ('percent', models.PositiveSmallIntegerField(blank=True, help_text="Un pourcentage à retirer du prix original, ne sera pas utilisé s'il y a un montant dans 'Montant fixe'.", null=True, verbose_name='Pourcentage')),
                ('is_active', models.BooleanField(default=True, verbose_name='Actif')),
                ('valid_from', models.DateTimeField(default=datetime.datetime.now, verbose_name='Date de début')),
                ('valid_until', models.DateTimeField(blank=True, null=True, verbose_name='Date de fin')),
            ],
            options={
                'verbose_name': 'Rabais par catégorie',
                'verbose_name_plural': 'Rabais par catégorie',
            },
        ),
    ]
