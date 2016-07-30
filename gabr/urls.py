from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from gabr import views
import django


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.post.feed, name='index'),
    url(r'^user/(?P<user_name>[^/]+)/following/$', views.profile.profile_following, name='profile_following'),
    url(r'^user/(?P<user_name>[^/]+)/followers/$', views.profile.profile_followers, name='profile_followers'),
    url(r'^user/(?P<user_name>[^/]+)/likes/$', views.profile.profile_likes, name='profile_likes'),
    url(r'^user/(?P<user_name>[^/]+)/lists/$', views.profile.profile_lists, name='profile_lists'),
    url(r'^user/(?P<user_name>[^/]+)/$', views.profile.profile_posts, name='profile'),
    url(r'^login/$', views.auth.login, name='login'),
    url(r'^logout/$', views.auth.logout, name='logout'),
    url(r'^signup/$', views.auth.signup, name='signup'),
    url(r'^new-post/$', views.post.new_post, name='new-post'),
    url(r'^post/(?P<post_id>[0-9]+)/$', views.post.view_post, name='post'),
    url(r'^tag/(?P<tag>.+)/$', views.post.feed, name='tag_feed'),
    url(r'^messages/$', views.post.feed, name='messages'),
    url(r'^notifications/$', views.notifications.notifications, name='notifications'),
    url(r'^help/$', views.post.feed, name='help'),
    url(r'^advertising/$', views.post.feed, name='advertising'),
    url(r'^settings/$', views.settings.settings, name='settings'),
    url(r'^ajax/like/$', views.post.ajax_like, name='ajax-like'),
    url(r'^ajax/repost/$', views.post.ajax_repost, name='ajax-repost'),
    url(r'^ajax/follow/$', views.profile.ajax_follow, name='ajax-follow'),
    url(r'^ajax/post/$', views.post.ajax_post, name='ajax-post'),
    url(r'^ajax/user/$', views.profile.ajax_user, name='ajax-user'),
    url(r'^ajax/load-posts/$', views.post.ajax_load_posts, name='ajax-load-posts'),
    url(r'^ajax/load-notification-count/$', views.notifications.ajax_load_notification_count,
        name='ajax-load-notification-count'),
    url(r'^ajax/load-trends/$', views.trends.ajax_load_trends, name='ajax-load-trends'),
    url(r'^ajax/check-posts/$', views.post.ajax_check_posts, name='ajax-check-posts'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', django.views.static.serve, { 'document_root': settings.MEDIA_ROOT }),
        url(r'^static/(?P<path>.*)$', django.views.static.serve, { 'document_root': settings.STATIC_ROOT, }),
    ]