from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy

from .forms import LoginForm, ResetPassword


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
                    return HttpResponseRedirect(reverse_lazy("main"))

        return render(request, 'login.html', {'form': form})

@login_required(login_url='/login/')
def default_redirect_view(request):
    # This view can be used as the default redirection view
    # when the 'next' parameter is not provided
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


def main(request):
    context = {}

    # user_agent = request.META['HTTP_USER_AGENT']

    # if 'Mobile' in user_agent:
    #     return render(request, 'mobile_main.html', context)
    # else:
    #     return render(request,  'main.html', context)

    return render(request, 'main.html', context)