from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from gabr.models import Profile, Follow, Post, Like, Notification, Trend
from gabr.forms import PostForm, SignupForm, LoginForm
import json


def profile_posts(request, username):
    current_user = None
    if request.user.is_authenticated():
        current_user = get_object_or_404(Profile, user=request.user)
    target_user = get_object_or_404(Profile, user__username=str.lower(username))

    context = {
        'current_user': current_user,
        'post_form': PostForm,
        'target_user': target_user,
        'is_following': False,
        'post_count': target_user.get_post_count(),
        'follow_count': target_user.get_follow_count(),
        'follower_count': target_user.get_follower_count(),
        'like_count': target_user.get_like_count(),
        'list_count': target_user.get_list_count(),
    }

    if request.user.is_authenticated():
        context['is_following'] = current_user.is_following(target_user)

    return render(request, 'profile-posts.html', context)


def profile_following(request, username):
    current_user = None
    if request.user.is_authenticated():
        current_user = get_object_or_404(Profile, user=request.user)
    target_user = get_object_or_404(Profile, user__username=str.lower(username))

    # FIXME: this is temp, move to ajax when JS profile card writer is done.
    follows = Follow.filter(subject=target_user)[:50]
    context_follows = []
    for follow in Follow.objects.filter(follower=target_user):
        pc, fc, flc = follow.subject.get_post_count(), follow.subject.get_follow_count(), follow.subject.get_follower_count()
        context_follows.append([follow.subject, pc, fc, flc])

    context = {
        'current_user': current_user,
        'post_form': PostForm,
        'target_user': target_user,
        'is_following': False,
        'post_count': target_user.get_post_count(),
        'follow_count': target_user.get_follow_count(),
        'follower_count': target_user.get_follower_count(),
        'like_count': target_user.get_like_count(),
        'list_count': target_user.get_list_count(),
        'follows': context_follows
    }

    if request.user.is_authenticated():
        context['is_following'] = current_user.is_following(target_user)

    return render(request, 'profile-following.html', context)


def profile_followers(request, username):
    current_user = None
    if request.user.is_authenticated():
        current_user = get_object_or_404(Profile, user=request.user)
    target_user = get_object_or_404(Profile, user__username=str.lower(username))

    # FIXME: this is temp, move to ajax when JS profile card writer is done.
    followers = []
    for follow in Follow.objects.filter(subject=target_user):
        pc, fc, flc = follow.follower.stats()
        followers.append([follow.follower, pc, fc, flc])

    context = {
        'current_user': current_user,
        'post_form': PostForm,
        'target_user': target_user,
        'is_following': False,
        'post_count': target_user.get_post_count(),
        'follow_count': target_user.get_follow_count(),
        'follower_count': target_user.get_follower_count(),
        'like_count': target_user.get_like_count(),
        'list_count': target_user.get_list_count(),
        'followers': followers,
    }

    if request.user.is_authenticated():
        context['is_following'] = current_user.is_following(target_user)

    return render(request, 'profile-followers.html', context)


def profile_likes(request, username):
    current_user = None
    if request.user.is_authenticated():
        current_user = get_object_or_404(Profile, user=request.user)
    target_user = get_object_or_404(Profile, user__username=str.lower(username))

    context = {
        'current_user': current_user,
        'post_form': PostForm,
        'target_user': target_user,
        'is_following': False,
        'post_count': target_user.get_post_count(),
        'follow_count': target_user.get_follow_count(),
        'follower_count': target_user.get_follower_count(),
        'like_count': target_user.get_like_count(),
        'list_count': target_user.get_list_count(),
    }

    if request.user.is_authenticated():
        context['is_following'] = current_user.is_following(target_user)

    return render(request, 'profile-likes.html', context)


def profile_lists(request, username):
    current_user = None
    if request.user.is_authenticated():
        current_user = Profile.objects.get(user=request.user)
    target_user = get_object_or_404(Profile, user__username=str.lower(username))

    context = {
        'current_user': current_user,
        'post_form': PostForm,
        'target_user': target_user,
        'is_following': False,
        'post_count': target_user.get_post_count(),
        'follow_count': target_user.get_follow_count(),
        'follower_count': target_user.get_follower_count(),
        'like_count': target_user.get_like_count(),
        'list_count': target_user.get_list_count(),
    }

    if request.user.is_authenticated():
        context['is_following'] = current_user.is_following(target_user)

    return render(request, 'profile-lists.html', context)
