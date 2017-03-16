import json
import re
import gabr.settings
from datetime import datetime, timedelta
from dateutil import tz
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from gabr.forms import PostForm
from gabr.models import Profile, Follow, Post, Like, Notification, Block, Report
from gabr.views.ajax_models import AjaxPost, AjaxUser

username_regex = re.compile('@(?P<username>[^\s]+)')


@login_required
def feed(request):
    current_user = AjaxUser(get_object_or_404(Profile, user=request.user))
    context = {
        'current_user': current_user,
        'post_form': PostForm,
        'debug_info': gabr.settings.get_debug_info(),
    }
    return render(request, 'feed.html', context)


def home(request):
    if request.user.is_authenticated():
        return feed(request)
    else:
        return render(request, 'landing.html')


def view_post(request, post_id):
    current_user = None
    if request.user.is_authenticated():
        current_user = Profile.objects.get(user=request.user)
    context = {
        'current-user': current_user,
        'post-form': PostForm,
        'post-id': post_id,
    }
    return render(request, 'post.html', context)
