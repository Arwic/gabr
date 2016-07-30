from user.models import UserProfile, Follow, Post, Like, Repost
from django import template
from django.http import HttpResponse, HttpResponseRedirect


register = template.Library()


@register.simple_tag
def has_liked(user, post):
    if not user.is_authenticated():
        return HttpResponseRedirect('/')
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/')

    return Like.objects.filter(user=user_profile, post=post).first() is not None


@register.simple_tag
def has_reposted(user, post):
    if not user.is_authenticated():
        return HttpResponseRedirect('/')
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/')

    return Repost.objects.filter(user=user_profile, post=post).first() is not None


@register.filter
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter
def add_class_placeholder(value, arg):
    s = arg.split('`')
    return value.as_widget(attrs={'class': s[0], 'placeholder': s[1]})
