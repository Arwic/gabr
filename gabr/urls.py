from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from user import urls as user_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(user_urls)),
]
