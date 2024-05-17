from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


from .forms import LoginForm, ResetPassword, AddEventForm
from .models import Event, EventImages, Organizer


class LoginView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form}
        return render(request, 'login.html', context)

    @staticmethod
    def post(request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

                # Redirect to the next URL if provided, otherwise, redirect to a default URL
                next_url = request.GET.get('next')

                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    # If 'next' parameter is not provided, redirect to a default URL
                    return HttpResponseRedirect(reverse_lazy("events"))

        return render(request, 'login.html', {'form': form})

@login_required(login_url='/login/')
def default_redirect_view(request):
    return HttpResponseRedirect(reverse_lazy('default_redirect_url'))


class ResetPasswordView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        form = ResetPassword(request.POST or None)
        form.initial['username'] = request.user.username
        context = {'form': form}
        return render(request, 'password_reset.html', context)

    @staticmethod
    def post(request, *args, **kwargs):
        current_user = request.user
        form = ResetPassword(request.POST or None)

        if form.is_valid():
            current_user.set_password(form.cleaned_data['new_password'])
            current_user.save()
            return HttpResponseRedirect('/')
        return render(request, 'password_reset.html', {'form': form})


def user_logout(request):
    request.user.set_unusable_password()
    logout(request)
    return HttpResponseRedirect('/')


def events_list(request):

    events = Event.objects.filter(is_active=True, published=True)

    context = {'events': events}

    # user_agent = request.META['HTTP_USER_AGENT']

    # if 'Mobile' in user_agent:
    #     return render(request, 'mobile_main.html', context)
    # else:
    #     return render(request,  'main.html', context)

    return render(request, 'main.html', context)


def add_event(request):
    if request.method == 'POST':

        event_form = AddEventForm(request.POST)
        if event_form.is_valid():

            if not request.user.groups.first() or not request.user.groups.first().organizer:
                error_message = "User is not an organizer!"
                return render(request, 'add_event.html',
                              {'event_form': event_form, 'error_message': error_message})

            event_organizer = request.user.groups.first().organizer

            event = Event.objects.create(organizer=event_organizer, **event_form.cleaned_data)

            if request.FILES:
                event.cover = request.FILES['cover']

            event.save()

            return redirect('events')

        else:
            error_message = event_form.errors
            return render(request, 'add_event.html',
                          {'ticket_form': event_form, 'error_message': error_message})

    else:
        event_form = AddEventForm()

        return render(request, 'add_event.html',
                      {'event_form': event_form})


def event_page(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    cover_orientation = event.get_cover_orientation()
    context = {'event': event, 'cover_orientation': cover_orientation}
    if event.user_is_event_organizer(request.user):
        return render(request, 'event_edit.html', context)
    else:
        return render(request, 'event_view.html', context)


def update_event(request, event_id):
    if request.method == 'POST':

        event_form = AddEventForm(request.POST)
        if event_form.is_valid():

            del event_form.cleaned_data['cover']
            event = Event.objects.get(id=event_id)

            if request.FILES.get('cover'):
                Event.objects.filter(id=event_id).update(**event_form.cleaned_data)
                event.cover = request.FILES.get('cover')
                event.save()
            else:
                Event.objects.filter(id=event_id).update(**event_form.cleaned_data, cover=event.cover)

            return redirect('events')

        else:
            error_message = event_form.errors
            return render(request, 'add_event.html',
                          {'ticket_form': event_form, 'error_message': error_message})


def add_event_image(request, event_id):

    event_object = Event.objects.get(id=event_id)

    if request.method == 'POST':

        image_desc = request.POST.get("image_desc")

        uploaded_file = request.FILES['image_file']

        extra_event_image = EventImages.objects.create(event=event_object, caption=image_desc, image=uploaded_file)

        extra_event_image.save()

    return redirect(reverse_lazy('event', args=[event_id]))


def remove_event_image(request, event_image_id):

    event_image_object = EventImages.objects.get(id=event_image_id)

    event = event_image_object.event

    event_image_object.delete()

    return redirect(reverse_lazy('event', args=[event.id]))



