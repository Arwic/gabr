import json
from django.shortcuts import get_object_or_404
from gabr.models import Profile, Post
from django.utils.dateformat import format


class AjaxUser:
    def __init__(self, user):
        if user is str:
            self.user = get_object_or_404(Profile, user__username=str.lower(user))
        else:
            self.user = user
        self.post_count = self.user.get_post_count()
        self.follow_count = self.user.get_follow_count()
        self.follower_count = self.user.get_follower_count()

    def get_dict(self):
        return {
            'id': self.user.id,
            'username': self.user.username,
            'display-name': self.user.display_name,
            'avatar-url': self.user.avatar.url,
            'banner-url': self.user.banner.url,
            'bio': self.user.bio,
            'gender': self.user.gender,
            'location': self.user.location,
            'website': self.user.website,
            'birthday': format(self.user.birthday, 'U'),
            'post-count': self.post_count,
            'follow-count': self.follow_count,
            'follower-count': self.follower_count,
        }

    def json(self):
        return json.dumps(self.get_dict())


class AjaxPost:
    def __init__(self, post, current_user=None):
        if post is int:
            self.post = get_object_or_404(Post, pk=post)
        else:
            self.post = post
        if current_user is not None:
            self.liked = current_user.has_liked(self.post)
        else:
            self.liked = False

    def get_dict(self):
        return {
            'id': self.post.id,
            'body': self.post.body,
            'time': format(self.post.time, 'U'),
            'user': AjaxUser(self.post.user).get_dict(),
            'liked': self.liked,
        }

    def json(self):
        return json.dumps(self.get_dict())
