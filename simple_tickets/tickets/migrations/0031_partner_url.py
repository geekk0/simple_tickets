# Generated by Django 5.0.2 on 2024-03-16 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0030_ticket_post_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name="Partner's URL"),
        ),
    ]