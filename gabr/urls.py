from django.conf.urls import include, url
from django.contrib import admin, auth
from django.contrib.auth.views import password_change, password_reset
from django.utils.functional import curry
from django.views.defaults import page_not_found, permission_denied, server_error

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
    url(r'^login/locked/$', views.auth.login_locked, name='login_locked'),
    url(r'^logout/$', views.auth.logout, name='logout'),
    url(r'^signup/$', views.auth.signup, name='signup'),
    url(r'^new-post/$', views.post.new_post, name='new-post'),
    url(r'^post/(?P<post_id>[0-9]+)/$', views.post.view_post, name='post'),
    url(r'^tag/(?P<tag>.+)/$', views.post.feed, name='tag_feed'),
    url(r'^messages/$', views.post.feed, name='messages'),
    url(r'^notifications/$', views.notifications.notifications, name='notifications'),
    url(r'^help/$', views.post.feed, name='help'),
    url(r'^advertising/$', views.post.feed, name='advertising'),
    url(r'^settings/$', views.settings.settings_profile, name='settings'),
    url(r'^settings/profile/$', views.settings.settings_profile, name='settings_profile'),
    url(r'^settings/account/$', views.settings.settings_account, name='settings_account'),
    url(r'^settings/password/$', django.contrib.auth.views.password_change,
        {
            'template_name': 'settings-password.html',
            'post_change_redirect': 'settings_password_success',
        }, name='settings_password'),
    url(r'^settings/password/success$', views.settings.settings_password_success, name='settings_password_success'),
    url(r'^settings/notifications/$', views.settings.settings_notifications, name='settings_notifications'),
    url(r'^settings/blocked/$', views.settings.settings_blocked, name='settings_blocked'),
    url(r'^settings/payment/$', views.settings.settings_payment, name='settings_payment'),
    url(r'^settings/apps/$', views.settings.settings_apps, name='settings_apps'),
    url(r'^settings/data/$', views.settings.settings_data, name='settings_data'),

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
    url(r'^ajax/report-user/$', views.post.ajax_report_user, name='ajax-report-user'),
    url(r'^ajax/block-user/$', views.post.ajax_block_user, name='ajax-block-user'),

    url(r'^ajax/get-thread/$', views.ajax.get_thread, name='ajax-get-thread'),
    url(r'^ajax/get-post/$', views.ajax.get_post, name='ajax-get-post'),
    url(r'^ajax/get-user-posts/$', views.ajax.get_user_posts, name='ajax-get-user-posts'),
    url(r'^ajax/get-user-feed/$', views.ajax.get_user_feed, name='ajax-get-user-feed'),
    url(r'^ajax/get-user-followers/$', views.ajax.get_user_followers, name='ajax-get-user-followers'),
    url(r'^ajax/get-user-following/$', views.ajax.get_user_following, name='ajax-get-user-following'),
    url(r'^ajax/get-user/$', views.ajax.get_user, name='ajax-get-user'),
]

handler500 = curry(server_error, template_name='500.html')
handler404 = curry(page_not_found, template_name='404.html')
handler403 = curry(permission_denied, template_name='403.html')

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', django.views.static.serve, { 'document_root': settings.MEDIA_ROOT }),
        url(r'^static/(?P<path>.*)$', django.views.static.serve, { 'document_root': settings.STATIC_ROOT, }),
    ]
