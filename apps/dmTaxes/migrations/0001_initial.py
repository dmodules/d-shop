# Generated by Django 2.2.17 on 2020-12-09 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CanadaTaxManagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('Alberta', 'Alberta'), ('British Columbia', 'British Columbia'), ('Manitoba', 'Manitoba'), ('New-Brunswick', 'New-Brunswick'), ('Newfoundland and Labrador', 'Newfoundland and Labrador'), ('Northwest Territories', 'Northwest Territories'), ('Nova Scotia', 'Nova Scotia'), ('Nunavut', 'Nunavut'), ('Ontario', 'Ontario'), ('Prince Edward Island', 'Prince Edward Island'), ('Quebec', 'Quebec'), ('Saskatchewan', 'Saskatchewan'), ('Yukon', 'Yukon')], max_length=60, unique=True, verbose_name='Province')),
                ('hst', models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True)),
                ('gst', models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True)),
                ('pst', models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True)),
                ('qst', models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True)),
                ('stripe_hst', models.CharField(blank=True, max_length=50, null=True)),
                ('stripe_gst', models.CharField(blank=True, max_length=50, null=True)),
                ('stripe_pst', models.CharField(blank=True, max_length=50, null=True)),
                ('stripe_qst', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Taxe canadienne',
                'verbose_name_plural': 'Taxes canadiennes',
            },
        ),
    ]
