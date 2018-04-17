from django.conf.urls import url
from previews import views


urlpatterns = [
    url(r'^$', views.ParserView.as_view()),
    url(r'^(.+)/', views.ParserView.as_view()),
]
