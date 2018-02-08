from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from commerce.models import Category, Item


class IndexView(TemplateView):
    template_name = 'index.html'

    extra_context = {'page_title': 'Магазин комиксов и фигурок THE EDGE'}


class CartView(TemplateView):
    template_name = 'commerce/cart.html'

    page_title = 'Корзина'

    extra_context = {'page_title': page_title}


class ItemView(TemplateView):
    template_name = 'commerce/item.html'

    page_title = 'Аккаунт'

    extra_context = {'page_title': page_title}
