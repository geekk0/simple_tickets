from django.contrib import admin

from .models import Ticket, Partner, Voucher, Package, TicketTemplate

admin.site.register(Ticket)
admin.site.register(Partner)
admin.site.register(Voucher)
admin.site.register(Package)
admin.site.register(TicketTemplate)
