from django.urls import path
from django.conf.urls import include
import previews.urls
import api.views


urlpatterns = [
    path('previews/', include(previews.urls), name='previews'),
    path('cloudinary/ping/', api.views.PingView.as_view(), name='cloudinary_ping'),
    path('cloudinary/usage/', api.views.UsageView.as_view(), name='cloudinary_usage'),
]
