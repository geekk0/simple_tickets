# Generated by Django 5.0.2 on 2024-04-27 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Event description'),
        ),
        migrations.AddField(
            model_name='organizer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Organizer email'),
        ),
        migrations.AddField(
            model_name='organizer',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Organizer phone'),
        ),
    ]
