from django.urls import path, include
import accounts.urls
import previews.urls
import accounts.views
import commerce.views


urlpatterns = [
    path('index/', commerce.views.IndexView.as_view(), name='index'),
    path('accounts/', include(accounts.urls), name='accounts'),
    path('cart/<action>', commerce.views.CartView.as_view(), name='cart_post'),
    path('cart/', commerce.views.CartView.as_view(), name='cart_get'),
    path('item/<id>/', commerce.views.ItemView.as_view(), name='item'),
    path('previews/', include(previews.urls), name='previews'),
]
