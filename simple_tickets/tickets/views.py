from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from .decorators import admin_required

from .models import Ticket, Voucher, Package, Partner, TicketTemplate
from .forms import TicketForm, VoucherFormSet
from ..events.models import Event


@admin_required
def add_tickets(request, event_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))

        ticket_form = TicketForm(request.POST)
        if ticket_form.is_valid():

            event = Event.objects.get(id=event_id)

            for i in range(quantity):
                ticket_holder = ticket_form.cleaned_data['holder']
                selected_package = ticket_form.cleaned_data['package']

                ticket = Ticket.objects.create(holder=ticket_holder, package=selected_package, event=event)
                ticket.save()
                ticket.create_qr_code()

                package = ticket.package

                if package:
                    for partner in package.partners.all():
                        voucher = Voucher.objects.create(ticket=ticket, partner=partner)
                        if partner.facilitator:
                            voucher.activities = True
                        voucher.save()

            return redirect(reverse_lazy('manage_tickets', args=[event.id]))

        # else:
        #     error_message = ticket_form.errors
        #     packages = Package.objects.all()
        #     return render(request, 'add_ticket.html',
        #                   {'ticket_form': ticket_form, 'packages': packages, 'error_message': error_message})

    # else:
    #     ticket_form = TicketForm()
    #     packages = Package.objects.all()
    #     event = Event.objects.get(id=event_id)
    #     return render(request, 'add_ticket.html',
    #                   {'ticket_form': ticket_form,
    #                    'packages': packages, 'event': event})


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


def manage_tickets(request, event_id):
    event = Event.objects.get(id=event_id)
    tickets = Ticket.objects.filter(event=event)
    packages = Package.objects.filter(event=event)
    partners = Partner.objects.filter(event=event, facilitator=False)
    facilitators = Partner.objects.filter(event=event, facilitator=True)

    context = {'event': event, 'tickets': tickets, 'packages': packages,
               'partners': partners, 'facilitators': facilitators}

    if 'show_facilitators_block' in request.session:
        context['show_facilitators_block'] = True
        del request.session['show_facilitators_block']
    else:
        context['show_facilitators_block'] = False

    return render(request, 'manage_tickets.html', context)


def update_package(request, event_id, package_id):

    if request.method == 'POST':

        name = request.POST.get("name")
        price = request.POST.get("package_price")
        package_partners_ids = request.POST.getlist("package_partners")
        package_partners = Partner.objects.filter(id__in=package_partners_ids)

        package_queryset = Package.objects.filter(id=package_id)
        package_queryset.update(name=name, price=price)
        package_queryset.first().partners.set(package_partners)

        return redirect(reverse_lazy('manage_tickets', args=[event_id]))


def update_tickets_template(request, event_id):
    if request.method == 'POST':
        new_tickets_template_image = request.FILES.get('tickets_template_image')
        ticket_template = TicketTemplate.objects.get(event=Event.objects.get(id=event_id))
        ticket_template.image = new_tickets_template_image
        ticket_template.save()
        return redirect(reverse_lazy('manage_tickets', args=[event_id]))


def add_package(request, event_id):
    if request.method == 'POST':
        new_package_name = request.POST.get("name")
        new_package_price = request.POST.get("package_price")
        new_package_partners_ids = request.POST.getlist("package_partners")
        new_package_partners = Partner.objects.filter(id__in=new_package_partners_ids)

        new_package = Package.objects.create(name=new_package_name, price=new_package_price,
                                             event=Event.objects.get(id=event_id))
        new_package.partners.set(new_package_partners)
        new_package.save()
        return redirect(reverse_lazy('manage_tickets', args=[event_id]))


def delete_package(request, package_id):
    package = Package.objects.get(id=package_id)
    package.delete()
    return redirect('manage_tickets', event_id=package.event.id)


def add_partner(request, event_id):
    if request.method == 'POST':
        new_partner_name = request.POST.get("name")
        new_partner_url = request.POST.get("email")
        new_partner_username = request.POST.get("username")
        new_partner_pass = request.POST.get("user_pass")
        new_partner_logo = request.FILES.get('image')
        new_partner_is_facilitator = request.POST.get('is_facilitator')

        new_partner_user = User.objects.create_user(username=new_partner_username,
                                                        password=new_partner_pass)
        new_partner_user.save()

        new_partner = Partner.objects.create(name=new_partner_name, url=new_partner_url,
                                             image=new_partner_logo,
                                             facilitator=new_partner_is_facilitator,
                                             user=new_partner_user)

        new_partner.event.set(Event.objects.filter(id=event_id))

        new_partner.save()

        request.session['show_facilitators_block'] = True

        return redirect(reverse_lazy('manage_tickets', args=[event_id]))
