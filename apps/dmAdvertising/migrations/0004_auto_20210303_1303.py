# Generated by Django 2.2.18 on 2021-03-03 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmAdvertising', '0003_auto_20210222_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dmadvertisingpopup',
            name='close_30days',
            field=models.BooleanField(default=True, help_text='Hide popup for 30 days on close, otherwise, show it everytime.', verbose_name='Hide for 30 days'),
        ),
        migrations.AlterField(
            model_name='dmadvertisingpopup',
            name='link',
            field=models.CharField(blank=True, help_text='Optional.', max_length=1000, null=True, verbose_name='URL Link'),
        ),
        migrations.AlterField(
            model_name='dmadvertisingpopup',
            name='title',
            field=models.CharField(help_text='Maximum 75 characters.', max_length=75, verbose_name='Title'),
        ),
    ]