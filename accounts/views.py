from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from accounts.models import User
from commerce.models import CartItem, Order


class AccountView(TemplateView):
    template_name = 'accounts/account.html'

    page_title = 'Аккаунт'

    def get(self, request):
        return render(request, self.template_name)
