import re

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from gabr.forms import PostForm, SettingsProfileForm
from gabr.models import UserProfile, Notification


http_link_re = re.compile(r'://')


@login_required
def settings_profile(request):
    current_user = get_object_or_404(UserProfile, user=request.user)
    form = SettingsProfileForm(request.POST or None, request.FILES or None, instance=current_user)
    if form.is_valid():
        instance = form.save(commit=False)
        if http_link_re.search(instance.website) is None:
            instance.website = "https://%s" % instance.website
        instance.save()
        return HttpResponseRedirect('/settings/profile/')
    context = {
        'current_user': current_user,
        'post_form': PostForm,
        'form': form,
    }
    return render(request, 'settings-profile.html', context)


@login_required
def settings_account(request):
    current_user = get_object_or_404(UserProfile, user=request.user)
    form = SettingsProfileForm(request.POST or None, request.FILES or None, instance=current_user)
    if form.is_valid():
        instance = form.save(commit=False)
        if http_link_re.search(instance.website) is None:
            instance.website = "https://%s" % instance.website

        instance.save()
        return HttpResponseRedirect('/')
    context = {
        'current_user': current_user,
        'post_form': PostForm,
        'form': form,
    }
    return render(request, 'settings-profile.html', context)


@login_required
def settings_notifications(request):
    current_user = get_object_or_404(UserProfile, user=request.user)
    form = SettingsProfileForm(request.POST or None, request.FILES or None, instance=current_user)
    if form.is_valid():
        instance = form.save(commit=False)
        if http_link_re.search(instance.website) is None:
            instance.website = "https://%s" % instance.website

        instance.save()
        return HttpResponseRedirect('/')
    context = {
        'current_user': current_user,
        'post_form': PostForm,
        'form': form,
    }
    return render(request, 'settings-profile.html', context)


@login_required
def settings_blocked(request):
    current_user = get_object_or_404(UserProfile, user=request.user)
    form = SettingsProfileForm(request.POST or None, request.FILES or None, instance=current_user)
    if form.is_valid():
        instance = form.save(commit=False)
        if http_link_re.search(instance.website) is None:
            instance.website = "https://%s" % instance.website

        instance.save()
        return HttpResponseRedirect('/')
    context = {
        'current_user': current_user,
        'post_form': PostForm,
        'form': form,
    }
    return render(request, 'settings-profile.html', context)


@login_required
def settings_payment(request):
    current_user = get_object_or_404(UserProfile, user=request.user)
    form = SettingsProfileForm(request.POST or None, request.FILES or None, instance=current_user)
    if form.is_valid():
        instance = form.save(commit=False)
        if http_link_re.search(instance.website) is None:
            instance.website = "https://%s" % instance.website

        instance.save()
        return HttpResponseRedirect('/')
    context = {
        'current_user': current_user,
        'post_form': PostForm,
        'form': form,
    }
    return render(request, 'settings-profile.html', context)


@login_required
def settings_apps(request):
    current_user = get_object_or_404(UserProfile, user=request.user)
    form = SettingsProfileForm(request.POST or None, request.FILES or None, instance=current_user)
    if form.is_valid():
        instance = form.save(commit=False)
        if http_link_re.search(instance.website) is None:
            instance.website = "https://%s" % instance.website

        instance.save()
        return HttpResponseRedirect('/')
    context = {
        'current_user': current_user,
        'post_form': PostForm,
        'form': form,
    }
    return render(request, 'settings-profile.html', context)


@login_required
def settings_data(request):
    current_user = get_object_or_404(UserProfile, user=request.user)
    form = SettingsProfileForm(request.POST or None, request.FILES or None, instance=current_user)
    if form.is_valid():
        instance = form.save(commit=False)
        if http_link_re.search(instance.website) is None:
            instance.website = "https://%s" % instance.website

        instance.save()
        return HttpResponseRedirect('/')
    context = {
        'current_user': current_user,
        'post_form': PostForm,
        'form': form,
    }
    return render(request, 'settings-profile.html', context)