from django.contrib import admin
from commerce.models import Category, Item, CartItem, Order, OrderStatus, PaymentMethod, DeliveryMethod, Publisher, PriceMap


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'publisher', 'price', 'active']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    pass


@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    pass


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'load_monthly', 'load_weekly']


@admin.register(PriceMap)
class PriceMapAdmin(admin.ModelAdmin):
    list_display = ['mode', 'usd', 'bought', 'default', 'discount', 'superior', 'weight']
