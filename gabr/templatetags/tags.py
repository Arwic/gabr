from gabr.models import UserProfile, Follow, Post, Like
from django import template
from django.http import HttpResponse, HttpResponseRedirect


register = template.Library()


@register.filter
def get_range(value):
    return range(value)
