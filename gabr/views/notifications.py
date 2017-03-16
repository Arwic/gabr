import json
from datetime import datetime, timedelta
import json

from dateutil import tz
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from gabr.forms import PostForm
from gabr.models import Profile, Notification


@login_required
def notifications(request):
    current_user = get_object_or_404(Profile, user=request.user)
    notifs = list(Notification.objects.filter(user=current_user))
    notifs.sort(key=lambda n: n.time, reverse=True)
    user_tz = tz.gettz(current_user.time_zone)
    for notif in notifs:
        notif.read = True
        notif.save()
        notif.time = notif.time.astimezone(user_tz)
    context = {
        'current_user': current_user,
        'post_form': PostForm,
        'notifications': notifs,
    }
    return render(request, 'notifications.html', context)


def ajax_load_notification_count(request):
    if not request.is_ajax():
        return HttpResponse('')
    if request.user.is_authenticated():
        current_user = Profile.objects.get(user=request.user)
        response = {
            'count': Notification.objects.filter(user=current_user, read=False).count()
        }
    else:
        response = {
            'count': 0
        }
    return HttpResponse(json.dumps(json.dumps(response)))
