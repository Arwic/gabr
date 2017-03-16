from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from os import path
import uuid
from django.utils.deconstruct import deconstructible
import datetime


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        return path.join(self.path, "%s.%s" % (uuid.uuid4().hex, ext))


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20, default='')
    display_name = models.CharField(max_length=20, default='')
    avatar = models.ImageField(upload_to=PathAndRename('avatars/'), default='/static/img/profile-default.png')
    banner = models.ImageField(upload_to=PathAndRename('banners/'), default='/static/img/banner-default.png')
    bio = models.CharField(max_length=160, blank=True, default='')
    gender = models.CharField(default='Male', max_length=6)
    location = models.CharField(max_length=30, blank=True, default='')
    website = models.CharField(max_length=100, blank=True, default='')
    birthday = models.DateField(default=datetime.date(1970, 1, 1), blank=True)
    time_zone = models.CharField(max_length=100, blank=True, default='Etc/GMT0')
    language = models.CharField(default='English', max_length=64)
    country = models.CharField(default='US', max_length=2)
    show_nsfw = models.BooleanField(default=False)

    def __str__(self):
        return self.user_name

    def get_follower_count(self):
        return Follow.objects.filter(subject=self).count()

    def get_follow_count(self):
        return Follow.objects.filter(follower=self).count()

    def get_post_count(self):
        return Post.objects.filter(user=self).count()

    def get_unread_notification_count(self):
        return Notification.objects.filter(user=self, read=False).count()

    def has_liked(self, post):
        try:
            Like.objects.get(user=self, post=post)
            return True
        except Like.DoesNotExist:
            return False

    def has_reposted(self, post):
        try:
            Post.objects.get(user=self, post__target=post)
            return True
        except Post.DoesNotExist:
            return False


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)


class Report(models.Model):
    reporter = models.ForeignKey(Profile, related_name='report_user_reporter', on_delete=models.CASCADE)
    subject = models.ForeignKey(Profile, related_name='report_user_subject', on_delete=models.CASCADE)
    message = models.CharField(default='', max_length=512)

    def __str__(self):
        return '@%s was reported by @%s: "%s"' % (self.subject.user_name, self.reporter.user_name, self.message)


class Block(models.Model):
    blocker = models.ForeignKey(Profile, related_name='block_user_blocker', on_delete=models.CASCADE)
    subject = models.ForeignKey(Profile, related_name='block_user_subject', on_delete=models.CASCADE)

    def __str__(self):
        return '@%s is blocking @%s' % (self.blocker.user_name, self.subject.user_name)


class Post(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    time = models.DateTimeField(default=datetime.datetime.utcnow)
    # used for reposts, left blank if not a repost
    target = models.ForeignKey('self', related_name='post_user_target', null=True, blank=True, default=None)
    # used for reply threads
    parent = models.ForeignKey('self', related_name='post_user_parent', null=True, blank=True, default=None)

    def __str__(self):
        return '@%s on %s says "%s"' % (self.user, self.time, self.body[:20])


class Follow(models.Model):
    class Meta:
        unique_together = ['follower', 'subject']
    follower = models.ForeignKey(Profile, related_name='user_follower', on_delete=models.CASCADE)
    subject = models.ForeignKey(Profile, related_name='user_subject', on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.datetime.utcnow)

    def save(self, *args, **kwargs):
        super(Follow, self).save()
        Notification.objects.create(notification_type='f', user=self.subject, follow=self)

    def __str__(self):
        return '@%s follows @%s' % (self.follower, self.subject)


class Like(models.Model):
    class Meta:
        unique_together = ['user', 'post']
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.datetime.utcnow)

    def save(self, *args, **kwargs):
        super(Like, self).save()
        Notification.objects.create(notification_type='l', user=self.post.user, like=self)

    def __str__(self):
        return '@%s liked %s' % (self.user, self.post)


NOTIFICATION_TYPE_CHOICES = [
    ('f', 'follow'),
    ('p', 'private message'),
    ('l', 'like'),
    ('m', 'mention'),
    ('r', 'repost'),
]


class Notification(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=1, choices=NOTIFICATION_TYPE_CHOICES)
    time = models.DateTimeField(default=datetime.datetime.utcnow)
    follow = models.ForeignKey(Follow, null=True, blank=True, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, null=True, blank=True, on_delete=models.CASCADE)
    like = models.ForeignKey(Like, null=True, blank=True, on_delete=models.CASCADE)
    mention = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE, related_name='mention')
    repost = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE, related_name='repost')

    def __str__(self):
        return '@%s has %s' % (self.user, self.notification_type)


class Trend(models.Model):
    tag = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.tag
