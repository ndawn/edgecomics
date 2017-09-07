from django.conf.urls import url
from previews import views


method_list = '(' + '|'.join(views.ParserView.method_list) + ')'


urlpatterns = [
    url(r'^$', views.ParserView.as_view()),
    url(r'^(.+)/', views.ParserView.as_view()),
]
