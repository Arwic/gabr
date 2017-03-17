from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from gabr.views.ajax_models import AjaxPost, AjaxProfile
from gabr.models import Profile, Trend, Post
import json
from datetime import datetime, timedelta


def user(request):
    if not request.is_ajax():
        return HttpResponse('')
    return HttpResponse(AjaxProfile(request['username']).json())


def post(request):
    if not request.is_ajax():
        return HttpResponse('')
    current_user = None
    if request.user.is_authenticated():
        current_user = get_object_or_404(Profile, user=request.user)
    parent_post = get_object_or_404(Post, pk=request.POST["post-id"])
    direct_replies = Post.objects.filter(parent=parent_post)
    response = {}
    response["main"] = AjaxPost(parent_post, current_user).get_dict()
    response["replies"] = []
    for reply in direct_replies:
        response["replies"].append(AjaxPost(reply, current_user).get_dict())
    return HttpResponse(json.dumps(response))


@login_required
def unread_notif_count(request):
    if not request.is_ajax():
        return HttpResponse('')
    notif_count = get_object_or_404(Profile, user=request.user).get_unread_notif_count()
    response = {
        'count': notif_count
    }
    return HttpResponse(json.dumps(response))


@login_required
def new_post_count(request):
    if not request.is_ajax():
        return HttpResponse('')
    current_user = get_object_or_404(Profile, user=request.user)
    time_newest = datetime.fromtimestamp(float(request.POST['time-newest']))
    post_count = len(Post.objects.filter(user=current_user, time__gt=time_newest))
    response = {
        'count': post_count,
    }
    return HttpResponse(json.dumps(response))


def trends(request):

    # FIXME: This adds some temp trends
    from gabr.models import Trend
    for t in Trend.objects.all():  # Drop all current trends
        t.delete()
    for i in range(8):  # Add new trends
        trend_tag = "Trend" + str(i)
        Trend.objects.create(tag=trend_tag)
    # END temp code

    if not request.is_ajax():
        return HttpResponse('')
    ajax_trends = []
    for trend in Trend.objects.all():
        ajax_trends.append(trend.tag)
    return HttpResponse(json.dumps(ajax_trends))
