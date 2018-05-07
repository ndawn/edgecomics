from django.contrib import admin
from django.urls import path, include
import jet.urls
import jet.dashboard.urls
import accounts.urls
import previews.urls
import accounts.views
import commerce.views


urlpatterns = [
    path('', commerce.views.IndexView.as_view(), name='index'),
    path('jet/', include(jet.urls, 'jet')),
    path('jet/dashboard/', include(jet.dashboard.urls, 'jet-dashboard')),
    path('accounts/', include(accounts.urls), name='accounts'),
    path('admin/', admin.site.urls),
    path('cart/<action>', commerce.views.CartView.as_view(), name='cart_post'),
    path('cart/', commerce.views.CartView.as_view(), name='cart_get'),
    path('item/<id>/', commerce.views.ItemView.as_view(), name='item'),
    path('previews/', include(previews.urls), name='previews'),
]
