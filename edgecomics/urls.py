from django.contrib import admin
from django.urls import path, include
import jet.urls
import jet.dashboard.urls
from edgecomics import api_urls


urlpatterns = [
    path('jet/', include(jet.urls, 'jet')),
    path('jet/dashboard/', include(jet.dashboard.urls, 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
]
