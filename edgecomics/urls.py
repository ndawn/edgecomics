from django.conf.urls import url, include
from django.contrib import admin
import previews.urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^previews/', include(previews.urls)),
]
