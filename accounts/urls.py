from django.urls import path
from accounts import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('recover/', views.RecoverView.as_view(), name='recover'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('profile/', views.AccountView.as_view(), name='profile'),
]
