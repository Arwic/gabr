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


class UserProfile(models.Model):
    user = models.OneToOneField(User)
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
    email_notif_like = models.BooleanField(default=True)
    email_notif_mention = models.BooleanField(default=True)
    email_notif_repost = models.BooleanField(default=True)
    email_notif_follow = models.BooleanField(default=True)
    email_notif_message = models.BooleanField(default=True)
    email_newsletter = models.BooleanField(default=True)

    def __str__(self):
        return self.user_name

    def stats(self):
        post_count = Post.objects.filter(user=self).count()
        follow_count = Follow.objects.filter(follower=self).count()
        follower_count = Follow.objects.filter(subject=self).count()
        return post_count, follow_count, follower_count

    def unread_notification_count(self):
        return Notification.objects.filter(user=self, read=False).count()

    def liked(self, post):
        try:
            Like.objects.get(user=self, post=post)
            return True
        except Like.DoesNotExist:
            return False

    def reposted(self, post):
        try:
            Repost.objects.get(user=self, post=post)
            return True
        except Repost.DoesNotExist:
            return False


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Report(models.Model):
    reporter = models.ForeignKey(UserProfile, related_name='report_user_reporter', on_delete=models.CASCADE)
    subject = models.ForeignKey(UserProfile, related_name='report_user_subject', on_delete=models.CASCADE)
    message = models.CharField(default='', max_length=512)

    def __str__(self):
        return '@%s was reported by @%s: "%s"' % (self.subject.user_name, self.reporter.user_name, self.message)


class Block(models.Model):
    blocker = models.ForeignKey(UserProfile, related_name='block_user_blocker', on_delete=models.CASCADE)
    subject = models.ForeignKey(UserProfile, related_name='block_user_subject', on_delete=models.CASCADE)

    def __str__(self):
        return '@%s is blocking @%s' % (self.blocker.user_name, self.subject.user_name)


class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    body = models.CharField(max_length=140)
    time = models.DateTimeField(default=datetime.datetime.utcnow)
    parent = models.ForeignKey('self', null=True, blank=True, default=None)

    def __str__(self):
        return '@%s on %s says "%s"' % (self.user, self.time, self.body[:20])


class Message(models.Model):
    user = models.ForeignKey(UserProfile, related_name='user_user', on_delete=models.CASCADE)
    target = models.ForeignKey(UserProfile, related_name='user_target', on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    time = models.DateTimeField(default=datetime.datetime.utcnow)
    read = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Message, self).save()
        Notification.objects.create(notification_type='p', user=self.target, message=self)

    def __str__(self):
        return '@%s to @%s says "%s"' % (self.user, self.target, self.body[:20])


class Follow(models.Model):
    class Meta:
        unique_together = ['follower', 'subject']
    follower = models.ForeignKey(UserProfile, related_name='user_follower', on_delete=models.CASCADE)
    subject = models.ForeignKey(UserProfile, related_name='user_subject', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Follow, self).save()
        Notification.objects.create(notification_type='f', user=self.subject, follow=self)

    def __str__(self):
        return '@%s follows @%s' % (self.follower, self.subject)


class Repost(models.Model):
    class Meta:
        unique_together = ['user', 'post']
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.datetime.utcnow)

    def save(self, *args, **kwargs):
        super(Repost, self).save()
        Notification.objects.create(notification_type='r', user=self.post.user, repost=self)

    def __str__(self):
        return '@%s reposted %s' % (self.user, self.post)


class Like(models.Model):
    class Meta:
        unique_together = ['user', 'post']
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
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
    ('r', 'repost'),
    ('m', 'mention'),
]


class Notification(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=1, choices=NOTIFICATION_TYPE_CHOICES)
    time = models.DateTimeField(default=datetime.datetime.utcnow)
    follow = models.ForeignKey(Follow, null=True, blank=True, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, null=True, blank=True, on_delete=models.CASCADE)
    like = models.ForeignKey(Like, null=True, blank=True, on_delete=models.CASCADE)
    repost = models.ForeignKey(Repost, null=True, blank=True, on_delete=models.CASCADE)
    mention = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE, related_name='mention')

    def __str__(self):
        return '@%s has %s' % (self.user, self.notification_type)


class Trend(models.Model):
    tag = models.CharField(max_length=160, default='')

    def __str__(self):
        return self.tag
