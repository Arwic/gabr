from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .ajax_models import AjaxPost, AjaxUser
from ..models import Profile, Trend, Post
import json


def user(request):
    if not request.is_ajax():
        return HttpResponse('')
    try:
        return HttpResponse(AjaxUser(request['username']).json())
    except:
        return HttpResponse('')


def post(request):
    if not request.is_ajax():
        return HttpResponse('')
    try:
        current_user = None
        if request.user.is_authenticated():
            current_user = get_object_or_404(Profile, user=request.user)
        return HttpResponse(AjaxPost(request['post-id'], current_user).json())
    except:
        return HttpResponse('')


@login_required
def unread_notification_count(request):
    if not request.is_ajax():
        return HttpResponse('')
    try:
        notification_count = get_object_or_404(Profile, user=request.user).get_unread_notification_count()
        response = {
            'count': notification_count
        }
        return HttpResponse(json.dumps(response))
    except:
        return HttpResponse('')


@login_required
def new_post_count(request):
    if not request.is_ajax():
        return HttpResponse('')
    try:
        current_user = get_object_or_404(Profile, user=request.user)
        time_oldest = int(request.POST['time-oldest'])
        time_newest = int(request.POST['time-newest'])
        post_count = len(Post.objects.filter(user=current_user, time__gt=time_oldest, time__lt=time_newest))
        response = {
            'count': post_count,
        }
        return HttpResponse(json.dumps(response))
    except:
        return HttpResponse('')


def trends(request):
    if not request.is_ajax():
        return HttpResponse('')
    try:
        trends = Trend.objects.all()
        ajax_trends = []
        for trend in trends:
            ajax_trends.append(trend.tag)
        return HttpResponse(json.dumps(ajax_trends))
    except:
        return HttpResponse('')
