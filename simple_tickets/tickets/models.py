import os
import secrets
import string

from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

from simple_tickets.events.models import Event

from .qrcodes import TicketQRCode
from .tg_bot import TelegramBot


class Partner(models.Model):
    name = models.CharField(verbose_name="Partner name", max_length=100)
    image = models.ImageField(upload_to='partner_images', null=True, blank=True)
    url = models.URLField(verbose_name="Partner's URL", null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="User")
    facilitator = models.BooleanField(verbose_name="Is facilitator", default=False)
    event = models.ManyToManyField(Event, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Patrners'


class Package(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    partners = models.ManyToManyField(Partner)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    code = models.CharField(max_length=100, verbose_name='Ticket unique number', unique=True, null=True, blank=True)
    vouchers = models.ForeignKey(Partner, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Vouchers')
    holder = models.CharField(max_length=250, verbose_name='Ticket holder name', blank=True, null=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, blank=True, null=True)
    number = models.IntegerField(verbose_name='Ticket number', unique=True, blank=True, null=True)
    qr_link = models.TextField(verbose_name='Link for QR code', blank=True, null=True)
    qr_image = models.ImageField(upload_to='qr_images', null=True, blank=True)
    ticket_image_template = models.ImageField(upload_to='ticket_image_templates', null=True, blank=True)
    image = models.ImageField(upload_to='tickets_images', null=True, blank=True)
    payment_status = models.CharField(max_length=20,
                                      choices=[('Paid', 'Paid'), ('Not paid', 'Not paid')],
                                      default='Not paid')
    payment_method = models.CharField(max_length=20,
                                      choices=[('Cash', 'Cash'), ('GCash', 'GCash')],
                                      default='Cash')
    post_discount = models.BooleanField(default=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Event')

    def __str__(self):
        return str(self.number)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        if not self.number:
            self.number = self.id
        if not self.qr_link:
            self.qr_link = f'http://141.8.195.70:8003/ticket_info/{self.code}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    @staticmethod
    def generate_unique_code():
        while True:
            code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(9))
            if not Ticket.objects.filter(code=code).exists():
                return code

    @staticmethod
    def send_all_tickets_info():
        tickets = Ticket.objects.all()
        info_txt = 'All tickets list:\n'
        for ticket in tickets:
            ticket_info_block = (f'number: {ticket.number}, code: {ticket.code}, holder: {ticket.holder},'
                                 f' \n qr_link: {ticket.qr_link};\n')
            info_txt += ticket_info_block
        telegram_bot = TelegramBot()
        telegram_bot.send_all_tickets(info_txt)

    @staticmethod
    def send_tickets_info_attached_to_partner():
        for partner in Partner.objects.all():
            info_txt = f'Partner: {partner.name}\n'
            vouchers = Voucher.objects.filter(partner=partner)
            for voucher in vouchers:
                ticket = voucher.ticket
                ticket_info_block = f'number: {ticket.number}, code: {ticket.code}, holder: {ticket.holder}\n'
                info_txt += ticket_info_block
            telegram_bot = TelegramBot()
            telegram_bot.send_all_tickets(info_txt)

    def create_qr_code(self):
        qr_code = TicketQRCode(self.qr_link)
        qr_code.create_qr_code_image()
        with open('qr_temp.png', 'rb') as f:
            data = f.read()
        self.qr_image.save(name="qr_temp.png", content=ContentFile(data))
        os.remove("qr_temp.png")


class TicketTemplate(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='ticket_template',
                                 null=True, blank=True)
    image = models.ImageField(upload_to='ticket_templates',
                              null=True, blank=True, verbose_name="Ticket template")


class Voucher(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('used', 'Used'),
    ]

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_vouchers', null=True, blank=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="Partner", null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"Voucher for {self.partner} (Ticket: {self.ticket.code})"

    class Meta:
        verbose_name = 'Voucher'
        verbose_name_plural = 'Vouchers'


