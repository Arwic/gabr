import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from gabr.forms import PostForm
from gabr.models import UserProfile, Notification, Trend


def ajax_load_trends(request):
    if not request.is_ajax():
        return HttpResponse('')

    trends = []
    for trend in Trend.objects.all():
        trends.append(trend.tag)

    response = {
        'trends': trends
    }

    return HttpResponse(json.dumps(json.dumps(response)))
