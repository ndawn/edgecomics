from django.urls import path
from previews import views


urlpatterns = [
    path('parse/', views.ParseView.as_view()),
    path('vk/', views.VKView.as_view()),
    path('price/', views.PriceView.as_view()),
]
