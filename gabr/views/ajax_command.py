import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from gabr.forms import PostForm
from gabr.models import Profile, Post, Like, Notification, Follow, Block, Report
import re


username_regex = re.compile('@(?P<username>[^\s]+)')


@login_required
def like_post(request):
    if not request.is_ajax():
        return HttpResponse('')
    post_id = request.POST['post-id']
    current_user = get_object_or_404(Profile, user=request.user)
    post = get_object_or_404(Post, id=post_id)
    try:
        like = Like.objects.get(post=post, user=current_user)
        like.delete()
        response = {
            'liked': False,
            'post-id': post_id,
        }
    except Like.DoesNotExist:
        Like.objects.create(user=current_user, post=post)
        response = {
            'liked': True,
            'post-id': post_id,
        }
    return HttpResponse(json.dumps(response))


@login_required
def follow_user(request):
    if not request.is_ajax():
        return HttpResponse('')
    current_user = get_object_or_404(Profile, user=request.user)
    print("\n\n\n\n\nFOLLOWING USERNAME=" + request.POST["username"] + "\n\n\n\n\n\n\n")
    user = get_object_or_404(Profile, username=request.POST['username'])
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
    target_user = get_object_or_404(Profile, username=str.lower(request.POST['target']))
    Report.objects.create(reporter=current_user, subject=target_user, message="NYI")
    return HttpResponse()


@login_required
def block_user(request):
    if not request.is_ajax():
        return HttpResponse('')
    current_user = get_object_or_404(Profile, user=request.user)
    target_user = get_object_or_404(Profile, username=str.lower(request.POST['target']))
    Block.objects.create(blocker=current_user, subject=target_user)
    return HttpResponse('')