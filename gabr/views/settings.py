import re

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from gabr.forms import PostForm, SettingsProfileForm, SettingsAccountForm, SettingsNotificationsForm
from gabr.models import UserProfile, Notification, Block


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
    form = SettingsAccountForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save(commit=True)
        return HttpResponseRedirect('/settings/account/')
    context = {
        'current_user': current_user,
        'post_form': PostForm,
        'form': form,
    }
    return render(request, 'settings-account.html', context)


@login_required
def settings_password_success(request):
    current_user = get_object_or_404(UserProfile, user=request.user)
    context = {
        'current_user': current_user,
        'post_form': PostForm,
        'state_success': True,
    }
    return render(request, 'settings-password.html', context)


@login_required
def settings_notifications(request):
    current_user = get_object_or_404(UserProfile, user=request.user)
    form = SettingsNotificationsForm(request.POST or None, instance=current_user)
    if form.is_valid():
        form.save(commit=True)
        return HttpResponseRedirect('/settings/notifications/')
    context = {
        'current_user': current_user,
        'post_form': PostForm,
        'form': form,
    }
    return render(request, 'settings-notifications.html', context)


@login_required
def settings_blocked(request):
    current_user = get_object_or_404(UserProfile, user=request.user)
    # get all blocked accounts
    blocks = Block.objects.filter(blocker=current_user)
    blocked_users = []
    for block in blocks:
        pc, fc, flc = block.subject.stats()
        blocked_users.append([block.subject, pc, fc, flc])
    context = {
        'blocked_users': blocked_users,
        'current_user': current_user,
        'post_form': PostForm,
    }
    return render(request, 'settings-blocked.html', context)


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
        form.save(commit=True)
        return HttpResponseRedirect('/settings/apps/')
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
        form.save(commit=False)
        return HttpResponseRedirect('/settings/data/')
    context = {
        'current_user': current_user,
        'post_form': PostForm,
        'form': form,
    }
    return render(request, 'settings-profile.html', context)