# Generated by Django 5.0.2 on 2024-03-04 09:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0013_alter_voucher_partner_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='tickets',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='tickets.ticket'),
        ),
        migrations.AlterField(
            model_name='package',
            name='vouchers',
            field=models.ManyToManyField(blank=True, null=True, to='tickets.voucher'),
        ),
    ]
