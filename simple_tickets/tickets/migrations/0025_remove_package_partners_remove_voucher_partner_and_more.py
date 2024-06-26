# Generated by Django 5.0.2 on 2024-03-08 09:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0024_ticket_qr_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='partners',
        ),
        migrations.RemoveField(
            model_name='voucher',
            name='partner',
        ),
        migrations.AddField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='tickets_images'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_image_template',
            field=models.ImageField(blank=True, null=True, upload_to='ticket_image_templates'),
        ),
        migrations.CreateModel(
            name='Facilitators',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Facilitator name')),
                ('image', models.ImageField(blank=True, null=True, upload_to='Facilitator_images')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Facilitator',
                'verbose_name_plural': 'Facilitators',
            },
        ),
        migrations.AddField(
            model_name='package',
            name='facilitators',
            field=models.ManyToManyField(to='tickets.facilitators'),
        ),
        migrations.AddField(
            model_name='voucher',
            name='facilitator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.facilitators', verbose_name='Facilitators'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='vouchers',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.facilitators', verbose_name='Vouchers'),
        ),
        migrations.DeleteModel(
            name='Partner',
        ),
    ]
