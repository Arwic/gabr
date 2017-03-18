from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from gabr.views.ajax_models import AjaxPost, AjaxProfile
from gabr.models import Profile, Trend, Post, Follow, Like
import json
from datetime import datetime, timedelta


thread_reply_limit = 25
post_fetch_limit = 50


@login_required
def feed(request):
    if not request.is_ajax():
        return HttpResponse('')
    current_user = get_object_or_404(Profile, user=request.user)
    time_oldest = datetime.fromtimestamp(float(request.POST['time-oldest']))
    posts = []
    # get posts from the people the user follows
    for follow in Follow.objects.filter(follower=current_user):
        for post in Post.objects.filter(user=follow.subject,
                                        time__lt=time_oldest).order_by('-time')[:post_fetch_limit]:
            posts.append(post)
    # get the user's own posts
    for post in Post.objects.filter(user=current_user,
                                    time__lt=time_oldest).order_by('-time')[:post_fetch_limit]:
        posts.append(post)
    # sort the posts
    posts.sort(key=lambda p: p.time, reverse=True)
    # only return the limit or less
    posts = posts[:post_fetch_limit]
    response = {}
    response['time-oldest'] = 2147483647
    response['time-newest'] = 0
    response['posts'] = []
    for post in posts:
        ap = AjaxPost(post, current_user)
        response['posts'].append(ap.get_dict())
        post_utime = post.time.timestamp()  # FIXME: this is casuing issues, needs to be an int unix time not string
        if response['time-oldest'] > post_utime:
            response['time-oldest'] = post_utime
        if response['time-newest'] < post_utime:
            response['time-newest'] = post_utime
    return HttpResponse(json.dumps(response))


def user_posts(request):
    if not request.is_ajax():
        return HttpResponse('')
    current_user = get_object_or_404(Profile, user=request.user)
    target_user = get_object_or_404(Profile, user__username=request['username'])
    time_oldest = request['time-oldest']
    time_newest = request['time-newest']
    response = []
    posts = Post.objects.filter(user=target_user, time__gt=time_oldest, time__lt=time_newest).order_by('-time')[:post_fetch_limit]
    for post in posts:
        response.append(AjaxPost(post, current_user).get_dict())
    return HttpResponse(json.dumps(response))


def user_likes(request):
    if not request.is_ajax():
        return HttpResponse('')
    current_user = get_object_or_404(Profile, user=request.user)
    target_user = get_object_or_404(Profile, user__username=request['username'])
    time_oldest = request['time-oldest']
    time_newest = request['time-newest']
    response = []
    likes = Like.objects.filter(user=target_user, time__gt=time_oldest, time__lt=time_newest).order_by('-time')[:post_fetch_limit]
    likes = likes
    for like in likes:
        response.append(AjaxPost(like.post, current_user).get_dict())
    return HttpResponse(json.dumps(response))


def user_follows(request):
    if not request.is_ajax():
        return HttpResponse('')
    target_user = get_object_or_404(Profile, user__username=request['username'])
    time_oldest = request['time-oldest']
    time_newest = request['time-newest']
    response = []
    follows = Follow.objects.filter(follower=target_user, time__gt=time_oldest, time__lt=time_newest).order_by('-time')[:post_fetch_limit]
    for follow in follows:
        response.append(AjaxProfile(follow.subject).get_dict())
    return HttpResponse(json.dumps(response))


def user_followers(request):
    if not request.is_ajax():
        return HttpResponse('')
    user = get_object_or_404(Profile, user__username=request['username'])
    time_oldest = request['time-oldest']
    time_newest = request['time-newest']
    response = []
    follows = Follow.objects.filter(subject=user, time__gt=time_oldest, time__lt=time_newest).order_by('-time')[:post_fetch_limit]
    for follow in follows:
        response.append(AjaxProfile(follow.follower).get_dict())
    return HttpResponse(json.dumps(response))


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
