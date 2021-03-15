# Generated by Django 2.2.18 on 2021-03-12 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmJobModule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dmjobdescription',
            name='joining',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Expected joining duration'),
        ),
        migrations.AddField(
            model_name='dmjobdescription',
            name='location',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Location'),
        ),
        migrations.AddField(
            model_name='dmjobdescription',
            name='salary',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Salary'),
        ),
        migrations.AddField(
            model_name='dmjobdescription',
            name='skills',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Skills'),
        ),
        migrations.AddField(
            model_name='dmjobdescription',
            name='training',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Training Required?'),
        ),
        migrations.AddField(
            model_name='dmjobdescription',
            name='work_schedule',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Work Schedule'),
        ),
    ]
