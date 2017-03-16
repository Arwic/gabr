from datetime import datetime, timedelta
import json

from dateutil import tz
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from gabr.forms import PostForm
from gabr.models import Profile, Follow, Post, Like, Notification, Block, Report
import re
import gabr.settings


username_regex = re.compile('@(?P<username>[^\s]+)')


def check_tags(post):
    tags = username_regex.findall(post.body)
    for username in tags:
        tagged_user = Profile.objects.filter(user__username=str.lower(username)).first()
        if tagged_user is None:
            print('user not found')
            continue
        Notification.objects.create(notification_type='m', user=tagged_user, mention=post)


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


class PostInfo:
    def __init__(self, is_repost, post, current_user):
        self.is_repost = is_repost
        self.current_user = current_user
        self.sort_time = post.time
        if is_repost:
            self.repost_user = post.user
            self.post = post.post
        else:
            self.post = post
        if self.current_user is not None:
            user_tz = tz.gettz(current_user.time_zone)
        else:
            user_tz = tz.gettz('Etc/GMT0')
        self.user_time = format_time(self.post.time.astimezone(user_tz), datetime.now(tz=user_tz))

    def json(self):
        post_json = {}
        post_json['repost'] = self.is_repost
        if self.is_repost:
            post_json['repost-user'] = {}
            post_json['repost-user']['id'] = self.repost_user.id
            post_json['repost-user']['user-name'] = self.repost_user.user_name
            post_json['repost-user']['display-name'] = self.repost_user.display_name
        post_json['post-user'] = {}
        post_json['post-user']['id'] = self.post.user.user.id
        post_json['post-user']['avatar'] = self.post.user.avatar.url
        post_json['post-user']['user-name'] = self.post.user.user_name
        post_json['post-user']['display-name'] = self.post.user.display_name

        post_json['post'] = {}
        post_json['post']['id'] = self.post.id
        post_json['post']['body'] = self.post.body
        post_json['post']['time'] = str(self.user_time)
        post_json['post']['liked'] = False
        post_json['post']['user-name'] = self.post.user.user_name
        if self.current_user is not None:
            post_json['post']['liked'] = self.current_user.liked(self.post)
        post_json['post']['reposted'] = False
        if self.current_user is not None:
            post_json['post']['reposted'] = self.current_user.reposted(self.post)
        return post_json


def get_feed_posts(current_user, time_oldest=datetime.fromtimestamp(0), time_newest=datetime.fromtimestamp(0)):
    posts = []
    # get posts from the people the use follows
    for follow in Follow.objects.filter(follower=current_user):
        for post in Post.objects.filter(user=follow.subject, time__gt=time_oldest, time__lt=time_newest) \
                .order_by('-time'):
            posts.append(PostInfo(False, post, current_user))
        for repost in Repost.objects.filter(user=follow.subject, time__gt=time_oldest, time__lt=time_newest) \
                .order_by('-time'):
            posts.append(PostInfo(True, repost, current_user))
    # get the user's own posts
    for post in Post.objects.filter(user=current_user, time__gt=time_oldest, time__lt=time_newest) \
            .order_by('-time'):
        posts.append(PostInfo(False, post, current_user))
    for repost in Repost.objects.filter(user=current_user, time__gt=time_oldest, time__lt=time_newest) \
            .order_by('-time'):
        posts.append(PostInfo(True, repost, current_user))
    return posts


def get_profile_posts(current_user, target_user, time_oldest, time_newest):
    posts = []
    for post in Post.objects.filter(user=target_user, time__gt=time_oldest, time__lt=time_newest) \
            .order_by('-time'):
        posts.append(PostInfo(False, post, current_user))
    for repost in Repost.objects.filter(user=target_user, time__gt=time_oldest, time__lt=time_newest) \
        .order_by('-time'):
        posts.append(PostInfo(True, repost, current_user))
    return posts


def get_profile_likes(current_user, target_user, time_oldest, time_newest):
    posts = []
    for like in Like.objects.filter(user=target_user, time__gt=time_oldest, time__lt=time_newest) \
            .order_by('-time'):
        posts.append(PostInfo(False, like.post, current_user))
    return posts


def feed(request):
    if request.user.is_authenticated():
        current_user = get_object_or_404(Profile, user=request.user)
    else:
        return render(request, 'landing.html')
    current_user_post_count, current_user_follow_count, current_user_follower_count = current_user.stats()
    context = {
        'current_user': current_user,
        'current_user_post_count': current_user_post_count,
        'current_user_follow_count': current_user_follow_count,
        'current_user_follower_count': current_user_follower_count,
        'post_form': PostForm,
        'debug_info': gabr.settings.get_debug_info(),
    }
    return render(request, 'feed.html', context)


def ajax_load_posts(request):
    if not request.is_ajax():
        return HttpResponse('')
    post_count = int(request.POST['count'])
    if post_count > 200:  # max 200
        post_count = 200
    time_oldest = datetime.fromtimestamp(int(request.POST['time-oldest']))
    time_newest = datetime.fromtimestamp(int(request.POST['time-newest']))
    request_type = request.POST['type']
    posts = []
    current_user = None
    if request.user.is_authenticated():
        current_user = get_object_or_404(Profile, user=request.user)
    if request_type == 'feed' and request.user.is_authenticated():
        posts = get_feed_posts(current_user, time_oldest, time_newest)
    elif request_type == 'profile-posts':
        target_user = get_object_or_404(Profile, user__username=str.lower(request.POST['target']))
        posts = get_profile_posts(current_user, target_user, time_oldest, time_newest)
    elif request_type == 'profile-likes':
        target_user = get_object_or_404(Profile, user__username=str.lower(request.POST['target']))
        posts = get_profile_likes(current_user, target_user, time_oldest, time_newest)
    posts.sort(key=lambda p: p.sort_time, reverse=True)
    posts = posts[:post_count]  # limit posts
    response = {}
    response['time-newest'] = 0
    response['time-oldest'] = 2147483647
    response['posts'] = []
    for post in posts:
        response['posts'].append(post.json())
        unix_time = int(post.post.time.strftime("%s"))
        if response['time-newest'] < unix_time:
            response['time-newest'] = unix_time + 1
        if response['time-oldest'] > unix_time:
            response['time-oldest'] = unix_time - 1
    return HttpResponse(json.dumps(json.dumps(response)))


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


@login_required
def new_post(request):
    current_user = get_object_or_404(Profile, user=request.user)
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = current_user
        try:
            print("trying to get parent post")
            parent_id = request.POST["new-post-modal-reply-target"]
            print("parent post id = " + parent_id)
            instance.parent = get_object_or_404(Post, id=parent_id)
        except:
            print("\n\nFAILED TO GET PARENT POST\n\n")
            for key in request.POST.items():
                print(key)
            pass
        instance.save()
        check_tags(instance)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def ajax_like(request):
    # check if we are authed and the request is ajax
    if not request.is_ajax():
        return HttpResponse('')

    post_id = request.POST['post_id']

    # try getting the user and the post objects
    try:
        user = Profile.objects.get(user=request.user)
        post = Post.objects.get(id=post_id)
    except Profile.DoesNotExist:
        return HttpResponse('')
    except Post.DoesNotExist:
        return HttpResponse('')

    # check if we should like or unlike the post
    try:
        like = Like.objects.get(post=post, user=user)
        like.delete()
        response = {
            'liked': False,
            'post_id': post_id,
        }
    except Like.DoesNotExist:
        like = Like.objects.create(user=user, post=post)
        response = {
            'liked': True,
            'post_id': post_id,
        }

    return HttpResponse(json.dumps(response))


@login_required
def ajax_repost(request):
    # check if we are authed and the request is ajax
    if not request.is_ajax():
        return HttpResponse('')

    post_id = request.POST['post_id']

    # try getting the user and the post objects
    try:
        user = Profile.objects.get(user=request.user)
        post = Post.objects.get(id=post_id)

        if user.id == post.user.id:
            return HttpResponse('')
    except Profile.DoesNotExist:
        return HttpResponse('')

    # check if we should like or unlike the post
    try:
        repost = Repost.objects.get(user=user, post=post)
        repost.delete()
        response = {
            'reposted': False,
            'post_id': post_id,
        }
    except Repost.DoesNotExist:
        repost = Repost.objects.create(user=user, post=post)
        response = {
            'reposted': True,
            'post_id': post_id,
        }

    return HttpResponse(json.dumps(response))


def ajax_post(request):
    # check if the request is ajax
    if not request.is_ajax():
        return HttpResponse('')
    current_user = None
    if request.user.is_authenticated():
        current_user = get_object_or_404(Profile, user=request.user)
    # get post data
    try:
        post_id = request.POST['post_id']
        post = Post.objects.get(id=post_id)
        post_count, following_count, follower_count = post.user.stats()
        response = {
            'user_name': post.user.user_name,
            'display_name': post.user.display_name,
            'avatar_url': post.user.avatar.url,
            'banner_url': post.user.banner.url,
            'time': format_time(post.time, datetime.now(tz=tz.gettz('Etc/GMT0'))),
            'body': post.body,
            'has_liked': False,
            'has_reposted': False,
        }

        # get replies
        reply_models = Post.objects.filter(parent=post)
        replies = []

        for reply in reply_models:
            post_info = PostInfo(False, reply, current_user)
            replies.append(post_info.json())

        response['replies'] = replies

        if request.user.is_authenticated():
            response['time'] = format_time(post.time, datetime.now(tz=tz.gettz(current_user.time_zone)));
            response['has_liked'] = current_user.liked(post)
            response['has_reposted'] = current_user.reposted(post)
    except Post.DoesNotExist:
        print("POST DOES NOT EXIST")
        return HttpResponse('')
    return HttpResponse(json.dumps(response))


@login_required
def ajax_check_posts(request):
    if not request.is_ajax():
        return HttpResponse('')
    current_user = get_object_or_404(Profile, user=request.user)
    time_oldest = datetime.fromtimestamp(int(request.POST['time-oldest']), tz=tz.tzutc())
    time_newest = datetime.fromtimestamp(int(request.POST['time-newest']), tz=tz.tzutc())
    posts = get_feed_posts(current_user, time_oldest, time_newest)
    response = {
        'count': len(posts),
    }
    return HttpResponse(json.dumps(response))


@login_required
def ajax_block_user(request):
    if not request.is_ajax():
        return HttpResponse('')
    current_user = get_object_or_404(Profile, user=request.user)
    target_user = get_object_or_404(Profile, user_name=str.lower(request.POST['target']))
    Block.objects.create(blocker=current_user, subject=target_user)
    response = {
    }
    return HttpResponse(json.dumps(response))


@login_required
def ajax_report_user(request):
    if not request.is_ajax():
        return HttpResponse('')
    current_user = get_object_or_404(Profile, user=request.user)
    target_user = get_object_or_404(Profile, user_name=str.lower(request.POST['target']))
    Report.objects.create(reporter=current_user, subject=target_user, message="NYI")
    response = {
    }
    return HttpResponse(json.dumps(response))
