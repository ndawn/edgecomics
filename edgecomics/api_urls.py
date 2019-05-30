from django.urls import path
from django.conf.urls import include
import accounts.urls
import commerce.urls
import previews.urls
import api.views


urlpatterns = [
    path('accounts/', include(previews.urls), name='accounts'),
    path('commerce/', include(previews.urls), name='commerce'),
    path('previews/', include(previews.urls), name='previews'),
    path('cloudinary/ping/', api.views.PingView.as_view(), name='cloudinary_ping'),
    path('cloudinary/usage/', api.views.UsageView.as_view(), name='cloudinary_usage'),
]
