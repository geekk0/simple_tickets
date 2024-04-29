from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .decorators import admin_required

from .models import Ticket, Voucher, Package
from .forms import TicketForm, VoucherFormSet


@admin_required
def add_ticket(request):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))

        ticket_form = TicketForm(request.POST)
        if ticket_form.is_valid():
            for i in range(quantity):
                ticket_holder = ticket_form.cleaned_data['holder']
                selected_package = ticket_form.cleaned_data['package']

                ticket = Ticket.objects.create(holder=ticket_holder, package=selected_package)
                ticket.save()
                ticket.create_qr_code()

                package = ticket.package

                if package:
                    for partner in package.partners.all():
                        voucher = Voucher.objects.create(ticket=ticket, partner=partner)
                        if partner.facilitator:
                            voucher.activities = True
                        voucher.save()

            return redirect('main')

        else:
            error_message = ticket_form.errors
            packages = Package.objects.all()
            return render(request, 'add_ticket.html',
                          {'ticket_form': ticket_form, 'packages': packages, 'error_message': error_message})

    else:
        ticket_form = TicketForm()
        packages = Package.objects.all()

        return render(request, 'add_ticket.html',
                      {'ticket_form': ticket_form,
                       'packages': packages})


def show_success_page(request):
    return render(request, 'success_page.html')


# def main(request):
#     context = {}
#
#     # user_agent = request.META['HTTP_USER_AGENT']
#
#     # if 'Mobile' in user_agent:
#     #     return render(request, 'mobile_main.html', context)
#     # else:
#     #     return render(request,  'main.html', context)
#
#     return render(request, 'main.html', context)


def ticket_info(request, ticket_code):
    try:
        ticket = Ticket.objects.get(code=ticket_code)

        if ticket.package:
            partners = ticket.package.partners.all()
            for partner in partners:
                if not Voucher.objects.filter(ticket=ticket, partner=partner).exists():
                    voucher = Voucher.objects.create(ticket=ticket, partner=partner)
                    voucher.save()
            vouchers = Voucher.objects.filter(ticket=ticket, partner__facilitator=False)
            activities = Voucher.objects.filter(ticket=ticket, partner__facilitator=True)
            packages = Package.objects.all()
            context = {'ticket_info': ticket, 'vouchers': vouchers,
                       'activities': activities, 'packages': packages}
        else:
            context = {'ticket_info': ticket}

    except Ticket.DoesNotExist:
        context = {'error': 'Ticket not found'}

    return render(request, 'ticket_info.html', context)


@login_required(login_url='/login/')
def update_ticket_vouchers(request, ticket_code):
    if request.method == 'POST':
        ticket = Ticket.objects.get(code=ticket_code)

        for prefix in request.POST:
            if prefix.startswith('voucher_status_'):
                voucher_id = prefix.replace('voucher_status_', '')
                voucher_status = request.POST[prefix]
                voucher = Voucher.objects.get(id=voucher_id)
                voucher.status = voucher_status
                voucher.save()
            elif prefix == 'package':
                ticket.package = Package.objects.get(id=request.POST[prefix])
            elif prefix == 'post_discount':
                ticket.post_discount = True
            elif 'csrf' not in prefix:
                ticket.post_discount = False
                setattr(ticket, prefix, request.POST[prefix])

        ticket.save()

    # return redirect('ticket_info', ticket_code=ticket_code)
    return ticket_info(request, ticket_code)


def send_all_tickets_info(request):
    Ticket.send_all_tickets_info()
    return redirect('main')


def send_tickets_info_attached_to_partner(request):
    Ticket.send_tickets_info_attached_to_partner()
    return redirect('main')
