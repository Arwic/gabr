import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from gabr.forms import PostForm
from gabr.models import Profile, Post, Like, Notification, Follow, Block, Report
import re


username_regex = re.compile('@(?P<username>[^\s]+)')


def _notify_tags(post):
    tags = username_regex.findall(post.body)
    for username in tags:
        tagged_user = Profile.objects.filter(user__username=str.lower(username)).first()
        if tagged_user is None:
            print('user not found')
            continue
        Notification.objects.create(notification_type='m', user=tagged_user, mention=post)


@login_required
def new_post(request):
    # TODO: "request.POST['field']" could cause issues, might have to be "request['field']"
    if not request.is_ajax():
        return HttpResponse('')
    current_user = get_object_or_404(Profile, user=request.user)
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = current_user
        try:
            parent_id = request.POST["new-post-modal-reply-target"]
            instance.parent = get_object_or_404(Post, id=parent_id)
        except:
            pass
        instance.save()
        _notify_tags(instance)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def like_post(request):
    # TODO: "request.POST['field']" could cause issues, might have to be "request['field']"
    if not request.is_ajax():
        return HttpResponse('')
    post_id = request['post_id']
    current_user = get_object_or_404(Profile, user=request.user)
    post = get_object_or_404(Post, id=post_id)
    try:
        like = Like.objects.get(post=post, user=current_user)
        like.delete()
        response = {
            'liked': False,
            'post_id': post_id,
        }
    except Like.DoesNotExist:
        Like.objects.create(user=current_user, post=post)
        response = {
            'liked': True,
            'post_id': post_id,
        }
    return HttpResponse(json.dumps(response))


@login_required
def follow_user(request):
    # TODO: "request.POST['field']" could cause issues, might have to be "request['field']"
    if not request.is_ajax():
        return HttpResponse('')
    current_user = get_object_or_404(Profile, user=request.user)
    user = get_object_or_404(Profile, user=request.user)
    try:
        follow = Follow.objects.get(follower=current_user, subject=user)
        follow.delete()
        response = {
            'following': False,
        }
    except Like.DoesNotExist:
        Follow.objects.create(follower=current_user, subject=user)
        response = {
            'following': True,
        }
    return HttpResponse(json.dumps(response))


@login_required
def report_post(request):
    if not request.is_ajax():
        return HttpResponse('')
    pass


@login_required
def report_user(request):
    if not request.is_ajax():
        return HttpResponse('')
    current_user = get_object_or_404(Profile, user=request.user)
    target_user = get_object_or_404(Profile, user_name=str.lower(request.POST['target']))
    Report.objects.create(reporter=current_user, subject=target_user, message="NYI")
    return HttpResponse()


@login_required
def block_user(request):
    if not request.is_ajax():
        return HttpResponse('')
    current_user = get_object_or_404(Profile, user=request.user)
    target_user = get_object_or_404(Profile, user_name=str.lower(request.POST['target']))
    Block.objects.create(blocker=current_user, subject=target_user)
    return HttpResponse('')