from datetime import datetime, timedelta
import json

import dateutil
from dateutil import tz
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from gabr.forms import PostForm
from gabr.models import Profile, Follow, Post, Like, Notification, Block, Report
import re
import gabr.settings


thread_reply_limit = 25
post_fetch_limit = 50


def validate_request(request):
    return request.is_ajax()


def get_replies(post):
    return Post.objects.filter(parent=post, limit=thread_reply_limit)


def get_current_user_profile(request):
    return get_object_or_404(Profile, user=request.user)


def json_dump_thread(thread_infos):
    thread_json = []
    for post in thread_infos:
        thread_json.append(post.json_dict())
    return json.dumps(thread_json)


def format_time(time, now):
    diff = now - time
    if diff > timedelta(hours=24):
        return time.strftime('%-d %b %Y')
    else:
        if diff <= timedelta(minutes=1):
            return '%ss' % diff.seconds
        elif diff <= timedelta(hours=1):
            return '%sm' % (diff.seconds // 60)
        elif diff <= timedelta(days=1):
            return '%sh' % (diff.seconds // 60 // 60)


class UserInfo:
    def __init__(self, user):
        if user is str:
            self.user = get_object_or_404(Profile, user__username=str.lower(user))
        else:
            self.user = user

    def json_dict(self):
        post_count, follow_count, follower_count = self.user.stats()
        return {
            'id': self.user.id,
            'display-name': self.user.display_name,
            'user-name': self.user.user_name,
            'avatar-url': self.user.avatar,
            'banner-url': self.user.banner,
            'bio': self.user.bio,
            'post-count': post_count,
            'follow-count': follow_count,
            'follower-count': follower_count,
        }

    def json_dump(self):
        return json.dumps(self.json_dict())


class PostInfo:
    def __init__(self, post, current_user, repost_user):
        self.post = post
        self.current_user = current_user
        self.repost_user = repost_user
        self.sort_time = post.time
        if self.current_user is not None:
            user_tz = tz.gettz(current_user.time_zone)
        else:
            user_tz = tz.gettz('Etc/GMT0')
        self.user_time = format_time(self.post.time.astimezone(user_tz), datetime.now(tz=user_tz))

    def json(self):
        return json.dumps({
            'id': self.post.id,
            'body': self.post.body,
            'time': str(self.user_time),
            'user': UserInfo(self.post.user.user_name).json_dict(),
            'liked': self.current_user.liked(self.post),
            'reposted': self.current_user.reposted(self.post),
        })


def get_post(request):
    if not validate_request(request):
        return HttpResponse('')
    try:
        current_user = get_current_user_profile(request)
        post_info = PostInfo(request['post-id'], get_object_or_404(Profile, user=request.user), current_user)
        return HttpResponse(post_info.json())
    except:
        return HttpResponse('')


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


def get_user(request):
    if not validate_request(request):
        return HttpResponse('')
    try:
        user_info = UserInfo(request['user-name'])
        return HttpResponse(user_info.json())
    except:
        return HttpResponse('')


def get_user_feed(request):
    if not validate_request(request):
        return HttpResponse('')
    try:
        current_user = get_current_user_profile(request)
        time_oldest = request['time-oldest']
        time_newest = request['time-newest']
        response = []
        # get posts from the people the use follows
        for follow in Follow.objects.filter(follower=current_user):
            for post in Post.objects.filter(user=follow.subject, time__gt=time_oldest, time__lt=time_newest).order_by('-time'):
                response.append(PostInfo(post, current_user, None))
        # get the user's own posts
        for post in Post.objects.filter(user=current_user, time__gt=time_oldest, time__lt=time_newest).order_by('-time'):
            response.append(PostInfo(post, current_user, None))
        return HttpResponse(json.dumps(response))
    except:
        return HttpResponse('')


def get_user_posts(request):
    if not validate_request(request):
        return HttpResponse('')
    try:
        current_user = get_current_user_profile(request)
        time_oldest = request['time-oldest']
        time_newest = request['time-newest']
        response = []
        for post in Post.objects.filter(user=current_user, time__gt=time_oldest, time__lt=time_newest).order_by('-time'):
            response.append(PostInfo(post, current_user, None))
        return HttpResponse(json.dumps(response))
    except:
        return HttpResponse('')


def get_user_likes(request):
    if not validate_request(request):
        return HttpResponse('')
    try:
        current_user = get_current_user_profile(request)
        time_oldest = request['time-oldest']
        time_newest = request['time-newest']
        response = []
        likes = Like.objects.filter(user=current_user, time__gt=time_oldest, time__lt=time_newest) \
            .order_by('-time')[:post_fetch_limit]
        for like in likes:
            response.append(PostInfo(like.post, current_user, None))
        return HttpResponse(json.dumps(response))
    except:
        return HttpResponse('')


def get_user_followers(request):
    if not validate_request(request):
        return HttpResponse('')
    try:
        current_user = get_current_user_profile(request)
        response = []
        followers = Follow.objects.filter(subject=current_user)[:]
        for follow in followers:
            response.append(UserInfo(follow.follower))
        return HttpResponse(json.dumps(response))
    except:
        return HttpResponse('')


def get_user_following(request):
    if not validate_request(request):
        return HttpResponse('')
    try:
        current_user = get_current_user_profile(request)
        response = []
        followings = Follow.objects.filter(follower=current_user)[:]
        for follow in followings:
            response.append(UserInfo(follow.subject))
        return HttpResponse(json.dumps(response))
    except:
        return HttpResponse('')
