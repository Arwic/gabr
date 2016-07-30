import re

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from user.forms import UserProfileForm, PostForm
from user.models import UserProfile, Notification


http_link_re = re.compile(r'://')


@login_required
def settings(request):
    current_user = get_object_or_404(UserProfile, user=request.user)
    form = UserProfileForm(request.POST or None, request.FILES or None, instance=current_user)
    if form.is_valid():
        instance = form.save(commit=False)
        if http_link_re.search(instance.website) is None:
            instance.website = "https://%s" % instance.website

        instance.save()
        return HttpResponseRedirect('/')
    unread_notif_count = Notification.objects.filter(user=current_user, read=False).count()
    context = {
        'current_user': current_user,
        'unread_notif_count': unread_notif_count,
        'post_form': PostForm,
        'form': form,
    }
    return render(request, 'settings.html', context)
