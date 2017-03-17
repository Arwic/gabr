import json
from django.shortcuts import get_object_or_404
from gabr.models import Profile, Post, User, Like
from django.utils.dateformat import format


class AjaxProfile:
    def __init__(self, profile):
        if type(profile) is Profile:
            self.profile = profile
        elif type(profile) is User:
            self.profile = get_object_or_404(Profile, user=profile)
        elif type(profile) is str:
            self.profile = get_object_or_404(Profile, user__username=str.lower(profile))
        else:
            raise ValueError("user must be a User object or a username string")
        self.post_count = self.profile.get_post_count()
        self.follow_count = self.profile.get_follow_count()
        self.follower_count = self.profile.get_follower_count()

    def get_dict(self):
        return {
            'id': self.profile.id,
            'username': self.profile.username,
            'display-name': self.profile.display_name,
            'avatar-url': self.profile.avatar.url,
            'banner-url': self.profile.banner.url,
            'bio': self.profile.bio,
            'gender': self.profile.gender,
            'location': self.profile.location,
            'website': self.profile.website,
            'birthday': format(self.profile.birthday, 'U'),
            'post-count': self.post_count,
            'follow-count': self.follow_count,
            'follower-count': self.follower_count,
        }

    def json(self):
        return json.dumps(self.get_dict())


class AjaxPost:
    def __init__(self, post, current_user=None):
        if type(post) is Post:
            self.post = post
        elif type(post) is str:
            self.post = get_object_or_404(Post, pk=str(post))
        elif type(post) is int:
            self.post = get_object_or_404(Post, pk=post)
        else:
            raise ValueError("post must be a Post object, or post id int/string")
        if current_user is not None:
            self.liked = current_user.has_liked(self.post)
        else:
            self.liked = False
        self.reply_count = self.post.get_reply_count()
        self.like_count = self.post.get_like_count()
        self.repost_count = self.post.get_repost_count()

    def get_dict(self):
        return {
            'id': self.post.id,
            'body': self.post.body,
            'time': format(self.post.time, 'U'),
            'user': AjaxProfile(self.post.user).get_dict(),
            'liked': self.liked,
            'reply-count': 0,
            'like-count': 0,
            'repost-count': 0
        }

    def json(self):
        return json.dumps(self.get_dict())
