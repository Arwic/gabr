from django.conf.urls import include, url
from django.contrib import admin, auth
from django.contrib.auth.views import password_change, password_reset
from django.utils.functional import curry
from django.views.defaults import page_not_found, permission_denied, server_error

from django.conf import settings
from gabr import views
import django


urlpatterns = [
    # admin
    url(r'^admin/', admin.site.urls),
    # settings
    url(r'^settings/$', views.settings.settings_profile, name='settings'),
    url(r'^settings/profile/$', views.settings.settings_profile, name='settings_profile'),
    url(r'^settings/account/$', views.settings.settings_account, name='settings_account'),
    url(r'^settings/password/$', django.contrib.auth.views.password_change, {
            'template_name': 'settings-password.html',
            'post_change_redirect': 'settings_password_success',
        }, name='settings_password'),
    url(r'^settings/password/success$', views.settings.settings_password_success, name='settings_password_success'),
    url(r'^settings/notifications/$', views.settings.settings_notifications, name='settings_notifications'),
    url(r'^settings/blocked/$', views.settings.settings_blocked, name='settings_blocked'),
    url(r'^settings/payment/$', views.settings.settings_payment, name='settings_payment'),
    url(r'^settings/apps/$', views.settings.settings_apps, name='settings_apps'),
    url(r'^settings/data/$', views.settings.settings_data, name='settings_data'),
    # auth
    url(r'^login/$', views.auth.login, name='login'),
    url(r'^login/locked/$', views.auth.login_locked, name='login_locked'),
    url(r'^logout/$', views.auth.logout, name='logout'),
    url(r'^signup/$', views.auth.signup, name='signup'),
    # personal feeds
    url(r'^messages/$', views.post.feed, name='messages'),
    url(r'^notifications/$', views.notifications.notifications, name='notifications'),
    url(r'^$', views.post.feed, name='index'),
    # general feeds
    url(r'^post/(?P<post_id>[0-9]+)/$', views.post.view_post, name='post'),
    url(r'^tag/(?P<tag>.+)/$', views.post.feed, name='tag_feed'),
    # user profile
    url(r'^user/(?P<username>[^/]+)/following/$', views.profile.profile_following, name='profile_following'),
    url(r'^user/(?P<username>[^/]+)/followers/$', views.profile.profile_followers, name='profile_followers'),
    url(r'^user/(?P<username>[^/]+)/likes/$', views.profile.profile_likes, name='profile_likes'),
    url(r'^user/(?P<username>[^/]+)/lists/$', views.profile.profile_lists, name='profile_lists'),
    url(r'^user/(?P<username>[^/]+)/$', views.profile.profile_posts, name='profile'),
    # articles
    url(r'^help/$', views.post.feed, name='help'),
    url(r'^advertising/$', views.post.feed, name='advertising'),
    # global forms
    url(r'^form/new-post/$', views.post.new_post, name='form-new-post'),
    # ajax command, allows the user to do something
    url(r'^ajax/command/like-post/$', views.ajax_command.like_post, name='ajax-action-like-post'),
    url(r'^ajax/command/follow-user/$', views.ajax_command.follow_user, name='ajax-action-follow-user'),
    url(r'^ajax/command/report-user/$', views.ajax_command.report_user, name='ajax-action-report-user'),
    url(r'^ajax/command/report-post/$', views.ajax_command.report_post, name='ajax-action-report-post'),
    url(r'^ajax/command/block-user/$', views.ajax_command.block_user, name='ajax-action-block-user'),
    # ajax get, gets a single item
    url(r'^ajax/get/user/$', views.ajax_get.user, name='ajax-get-user'),
    url(r'^ajax/get/post/$', views.ajax_get.post, name='ajax-get-post'),
    url(r'^ajax/get/trends/$', views.ajax_get.trends, name='ajax-get-trends'),
    url(r'^ajax/get/unread-notif-count/$', views.ajax_get.unread_notif_count, name='ajax-get-unread-notification-count'),
    url(r'^ajax/get/new-post-count/$', views.ajax_get.new_post_count, name='ajax-get-new-post-count'),
    # ajax feed, gets a list of items
    url(r'^ajax/feed/main/$', views.ajax_feed.main, name='ajax-feed-main'),
    url(r'^ajax/feed/user-posts/$', views.ajax_feed.user_posts, name='ajax-feed-user-posts'),
    url(r'^ajax/feed/user-followers/$', views.ajax_feed.user_followers, name='ajax-feed-user-followers'),
    url(r'^ajax/feed/user-follows/$', views.ajax_feed.user_follows, name='ajax-feed-user-follows'),
    url(r'^ajax/feed/user-likes/$', views.ajax_feed.user_likes, name='ajax-feed-user-likes'),
    # FIXME: old
    #url(r'^ajax/load-posts/$', views.post.ajax_load_posts, name='ajax-load-posts'),
]

handler500 = curry(server_error, template_name='500.html')
handler404 = curry(page_not_found, template_name='404.html')
handler403 = curry(permission_denied, template_name='403.html')

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', django.views.static.serve, { 'document_root': settings.MEDIA_ROOT }),
        url(r'^static/(?P<path>.*)$', django.views.static.serve, { 'document_root': settings.STATIC_ROOT, }),
    ]
