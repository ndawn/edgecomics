from django.contrib import admin
from django.urls import path
from django.conf.urls import include
import accounts.views
import commerce.views
import api.views


urlpatterns = [
    path('', commerce.views.IndexView.as_view(), name='index'),
    path('api/cart/<method>/', api.views.CartView.as_view()),
    path('api/cart/', api.views.CartView.as_view()),
    path('account/', accounts.views.AccountView.as_view(), name='account'),
    path('admin/', admin.site.urls),
    path('cart/', commerce.views.CartView.as_view(), name='cart'),
    path('item/<id>/', commerce.views.ItemView.as_view(), name='cart'),
]
