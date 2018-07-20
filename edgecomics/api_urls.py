from django.urls import path
from django.conf.urls import include
import previews.urls


urlpatterns = [
    path('previews/', include(previews.urls), name='previews'),
]
