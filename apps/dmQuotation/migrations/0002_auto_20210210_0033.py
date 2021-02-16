# Generated by Django 2.2.17 on 2021-02-10 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dshop', '0053_auto_20210205_1127'),
        ('dmQuotation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dmquotation',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='dshop.Customer'),
        ),
        migrations.AlterField(
            model_name='dmquotation',
            name='number',
            field=models.CharField(max_length=100, verbose_name='Quotation Number'),
        ),
    ]