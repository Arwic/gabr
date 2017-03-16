from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from axes.utils import reset
from django.core.urlresolvers import reverse_lazy
from axes.decorators import watch_login
from gabr.models import Profile


from gabr.forms import SignupForm, LoginForm, AxesCaptchaForm


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@watch_login
def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = str.lower(form.cleaned_data['username'])
        password = form.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/')
    context = {
        'form': form
    }
    return render(request, 'login.html', context)


def login_locked(request):
    if request.POST:
        form = AxesCaptchaForm(request.POST)
        if form.is_valid():
            ip = get_client_ip(request)
            reset(ip=ip)
            return HttpResponseRedirect(reverse_lazy('login'))
    else:
        form = AxesCaptchaForm()
    context = {
        'form': form
    }
    return render(request, 'login_locked.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def signup(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        password2 = form.cleaned_data["confirm_password"]
        display_name = form.cleaned_data["display_name"]
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        gender = form.cleaned_data["gender"]
        if password == password2:
            user = User.objects.create_user(str.lower(username), email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            user = get_object_or_404(Profile, user=user)
            user.display_name = display_name
            user.user_name = username
            user.gender = gender
            user.save()
            return HttpResponseRedirect('/')
    context = {
        'form': form
    }
    return render(request, 'signup.html', context)
