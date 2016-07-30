from django.contrib import admin
from .models import *


admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Repost)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(Trend)
