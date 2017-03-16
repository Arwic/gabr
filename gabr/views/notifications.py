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
    for notif in notifs:
        notif.read = True
        notif.save()
    context = {
        'current_user': current_user,
        'post_form': PostForm,
        'notifications': notifs,
    }
    return render(request, 'notifications.html', context)
