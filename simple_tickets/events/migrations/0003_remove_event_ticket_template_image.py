# Generated by Django 5.0.2 on 2024-04-27 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_description_organizer_email_organizer_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='ticket_template_image',
        ),
    ]