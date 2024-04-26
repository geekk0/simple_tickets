# Generated by Django 5.0.2 on 2024-03-05 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0020_ticket_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='qr_link',
            field=models.TextField(blank=True, null=True, verbose_name='Link for QR code'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='code',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Ticket unique number'),
        ),
    ]
