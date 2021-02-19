# Generated by Django 2.2.18 on 2021-02-19 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dmShipping', '0005_auto_20210118_0921'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingCountry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Maximum 50 characters.', max_length=50, verbose_name='Country Name')),
                ('code', models.CharField(help_text='Maximum 2 characters.', max_length=10, unique=True, verbose_name='Country Code')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Maximum 50 characters.', max_length=50, verbose_name='State Name')),
                ('code', models.CharField(help_text='Maximum 2 characters.', max_length=10, unique=True, verbose_name='State Code')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dmShipping.ShippingCountry', verbose_name='Country')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingCity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Maximum 50 characters.', max_length=50, verbose_name='City Name')),
                ('code', models.CharField(help_text='Maximum 2 characters.', max_length=10, unique=True, verbose_name='City Code')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dmShipping.ShippingState', verbose_name='State')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAllowed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=3, help_text='An amount to be added to the cart price.', max_digits=30, verbose_name='Price')),
                ('cities', models.ManyToManyField(to='dmShipping.ShippingCity', verbose_name='Cities')),
                ('countries', models.ManyToManyField(to='dmShipping.ShippingCountry', verbose_name='Countries')),
                ('shipping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dmShipping.ShippingManagement', verbose_name='Shipping Management')),
                ('states', models.ManyToManyField(to='dmShipping.ShippingState', verbose_name='States')),
            ],
        ),
    ]
