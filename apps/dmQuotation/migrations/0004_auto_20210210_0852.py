# Generated by Django 2.2.17 on 2021-02-10 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmQuotation', '0003_auto_20210210_0827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dmquotation',
            name='session_id',
        ),
        migrations.AddField(
            model_name='dmquotation',
            name='cookie',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Cookie ID'),
        ),
    ]
