# Generated by Django 2.2.17 on 2021-01-04 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmBillingStripe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stripeorderdata',
            name='receipt_url',
            field=models.CharField(max_length=1000, verbose_name="Receipt's URL"),
        ),
        migrations.AlterField(
            model_name='stripeorderdata',
            name='stripe_payment_data',
            field=models.TextField(verbose_name="Stripe's Payment Data"),
        ),
        migrations.AlterField(
            model_name='stripeorderdata',
            name='stripe_session_data',
            field=models.TextField(verbose_name="Stripe's Data"),
        ),
    ]