from datetime import datetime, timedelta
import json
from dateutil import tz
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from gabr.models import Profile, Follow, Post, Like
from .ajax_models import AjaxPost, AjaxUser
from django.contrib.auth.decorators import login_required

thread_reply_limit = 25
post_fetch_limit = 50


def _get_replies(post):
    # TODO: this needs to have variants like most recent and best rated etc.
    return Post.objects.filter(parent=post, limit=thread_reply_limit)


def _post_list_json(posts):
    posts_json = []
    for post in posts:
        posts_json.append(post.json_dict())
    return json.dumps(posts_json)

'''
def get_thread(request):
    if not validate_request(request):
        return HttpResponse('')
    try:
        current_user = get_current_user_profile(request)
        post_info = PostInfo(request['post-id'], current_user, None)
        parent_info = PostInfo(post_info.post.parent, current_user, None)
        replies = get_replies(post_info.post)
        reply_infos = []
        for r in replies:
            reply_infos.append(PostInfo(r, current_user, None))
        thread = [parent_info, post_info, *reply_infos]
        thread_json = json_dump_thread(thread)
        return HttpResponse(thread_json)
    except:
        return HttpResponse('')
'''


@login_required
def main(request):
    if not request.is_ajax():
        return HttpResponse('')
    try:
        current_user = get_object_or_404(Profile, user=request.user)
        time_oldest = request['time-oldest']
        time_newest = request['time-newest']
        posts = []
        # get posts from the people the user follows
        for follow in Follow.objects.filter(follower=current_user):
            for post in Post.objects.filter(user=follow.subject, time__gt=time_oldest, time__lt=time_newest).order_by('-time')[:post_fetch_limit]:
                posts.append(post)
        # get the user's own posts
        for post in Post.objects.filter(user=current_user, time__gt=time_oldest, time__lt=time_newest).order_by('-time')[:post_fetch_limit]:
            posts.append(post)
        # sort the posts
        posts.sort(key=lambda p: p.time, reverse=True)
        # only return the limit or less
        posts = posts[:post_fetch_limit]
        response = {}
        response['time-newest'] = 0
        response['time-oldest'] = 2147483647
        response['posts'] = []
        for post in posts:
            response['posts'].append(AjaxPost(post, current_user).get_dict())
            unix_time = int(post.post.time.strftime("%s"))
            if response['time-newest'] < unix_time:
                response['time-newest'] = unix_time + 1
            if response['time-oldest'] > unix_time:
                response['time-oldest'] = unix_time - 1
        return HttpResponse(json.dumps(response))
    except:
        return HttpResponse('')


def user_posts(request):
    if not request.is_ajax():
        return HttpResponse('')
    try:
        current_user = get_object_or_404(Profile, user=request.user)
        target_user = get_object_or_404(Profile, user__username=request['username'])
        time_oldest = request['time-oldest']
        time_newest = request['time-newest']
        response = []
        posts = Post.objects.filter(user=target_user, time__gt=time_oldest, time__lt=time_newest).order_by('-time')[:post_fetch_limit]
        for post in posts:
            response.append(AjaxPost(post, current_user).get_dict())
        return HttpResponse(json.dumps(response))
    except:
        return HttpResponse('')


def user_likes(request):
    if not request.is_ajax():
        return HttpResponse('')
    try:
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
    except:
        return HttpResponse('')


def user_follows(request):
    if not request.is_ajax():
        return HttpResponse('')
    try:
        target_user = get_object_or_404(Profile, user__username=request['username'])
        time_oldest = request['time-oldest']
        time_newest = request['time-newest']
        response = []
        follows = Follow.objects.filter(follower=target_user, time__gt=time_oldest, time__lt=time_newest).order_by('-time')[:post_fetch_limit]
        for follow in follows:
            response.append(AjaxUser(follow.subject).get_dict())
        return HttpResponse(json.dumps(response))
    except:
        return HttpResponse('')


def user_followers(request):
    if not request.is_ajax():
        return HttpResponse('')
    try:
        user = get_object_or_404(Profile, user__username=request['username'])
        time_oldest = request['time-oldest']
        time_newest = request['time-newest']
        response = []
        follows = Follow.objects.filter(subject=user, time__gt=time_oldest, time__lt=time_newest).order_by('-time')[:post_fetch_limit]
        for follow in follows:
            response.append(AjaxUser(follow.follower).get_dict())
        return HttpResponse(json.dumps(response))
    except:
        return HttpResponse('')
