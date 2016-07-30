from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from gabr.models import UserProfile, Follow, Post, Like, Repost, Notification, Trend
from gabr.forms import UserProfileForm, PostForm, SignupForm, MessageForm, LoginForm
import json
import datetime
from dateutil import tz


def is_following(follower_profile, subject_profile):
    try:
        Follow.objects.get(follower=follower_profile, subject=subject_profile)
        return True
    except Follow.DoesNotExist:
        return False


def get_stats(user_profile):
    post_count = Post.objects.filter(user=user_profile).count()
    follow_count = Follow.objects.filter(follower=user_profile).count()
    follower_count = Follow.objects.filter(subject=user_profile).count()
    return post_count, follow_count, follower_count


def profile_posts(request, user_name):
    current_user = UserProfile.objects.get(user=request.user)
    target_user = get_object_or_404(UserProfile, user__username=user_name)

    # posts = get_user_post_infos(current_user, target_user)

    post_count, follow_count, follower_count = target_user.stats()
    like_count = len(Like.objects.filter(user=target_user))
    list_count = 0  # TODO: implements lists

    context = {
        'current_user': current_user,
        'unread_notif_count': current_user.unread_notification_count(),
        'post_form': PostForm,
        'target_user': target_user,
        'is_following': is_following(current_user, target_user),
        'post_count': post_count,
        'follow_count': follow_count,
        'follower_count': follower_count,
        'like_count': like_count,
        'list_count': list_count,
    }

    return render(request, 'profile-posts.html', context)


def profile_following(request, user_name):
    current_user = UserProfile.objects.get(user=request.user)
    target_user = get_object_or_404(UserProfile, user__username=user_name)

    post_count, follow_count, follower_count = target_user.stats()
    like_count = len(Like.objects.filter(user=target_user))
    list_count = 0  # TODO: implements lists

    follows = []
    for follow in Follow.objects.filter(follower=target_user):
        post_count, follow_count, follower_count = follow.subject.stats()
        follows.append([follow.subject, post_count, follow_count, follower_count])

    context = {
        'current_user': current_user,
        'unread_notif_count': current_user.unread_notification_count(),
        'post_form': PostForm,
        'target_user': target_user,
        'follows': follows,
        'is_following': is_following(current_user, target_user),
        'post_count': post_count,
        'follow_count': follow_count,
        'follower_count': follower_count,
        'like_count': like_count,
        'list_count': list_count,
    }

    return render(request, 'profile-following.html', context)


def profile_followers(request, user_name):
    current_user = UserProfile.objects.get(user=request.user)
    target_user = get_object_or_404(UserProfile, user__username=user_name)

    context = {
        'current_user': current_user,
        'unread_notif_count': current_user.unread_notification_count(),
        'post_form': PostForm,
        'target_user': target_user,
        'is_following': is_following(current_user, target_user),
    }

    return render(request, 'profile-followers.html', context)


def profile_likes(request, user_name):
    current_user = UserProfile.objects.get(user=request.user)
    target_user = get_object_or_404(UserProfile, user__username=user_name)

    context = {
        'current_user': current_user,
        'unread_notif_count': current_user.unread_notification_count(),
        'post_form': PostForm,
        'target_user': target_user,
        'is_following': is_following(current_user, target_user),
    }

    return render(request, 'profile-likes.html', context)


def profile_lists(request, user_name):
    current_user = UserProfile.objects.get(user=request.user)
    target_user = get_object_or_404(UserProfile, user__username=user_name)

    context = {
        'current_user': current_user,
        'unread_notif_count': current_user.unread_notification_count(),
        'post_form': PostForm,
        'target_user': target_user,
        'is_following': is_following(current_user, target_user),
    }

    return render(request, 'profile-lists.html', context)


@login_required
def ajax_follow(request):
    # check if we are authed and the request is ajax
    if not request.is_ajax():
        return HttpResponse('')
    # get user data
    target_username = request.POST['user_name']
    try:
        user = get_object_or_404(UserProfile, user=request.user)
        target = get_object_or_404(UserProfile, user__username=target_username)
    except UserProfile.DoesNotExist:
        return HttpResponse('')
    # get follow data
    try:
        follow = Follow.objects.get(follower=user, subject=target)
        # we are already following them, lets unfollow
        follow.delete()
        response = {
            'follow': False,
            'user_name': target_username,
        }
    except Follow.DoesNotExist:
        # we are not following them yet, lets follow
        follow = Follow.objects.create(follower=user, subject=target)
        response = {
            'follow': True,
            'user_name': target_username,
        }
    return HttpResponse(json.dumps(response))


def ajax_user(request):
    # check if the request is ajax
    if not request.is_ajax():
        return HttpResponse('')
    # get post data
    try:
        user_profile = get_object_or_404(UserProfile, user__username=request.POST['user_name'])
        post_count, following_count, follower_count = user_profile.stats()
        post_info = {
            'display_name': user_profile.display_name,
            'bio': user_profile.bio,
            'banner_url': user_profile.banner.url,
            'avatar_url': user_profile.avatar.url,
            'post_count': post_count,
            'following_count': following_count,
            'follower_count': follower_count,
        }
    except UserProfile.DoesNotExist:
        return HttpResponse('')
    return HttpResponse(json.dumps(post_info))
