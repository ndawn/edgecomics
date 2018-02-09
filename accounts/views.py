from django.views.generic import View, TemplateView
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.models import User
from commerce.models import Cart


class AccountView(TemplateView):
    """TemplateView for displaying account profile page

    Requires to be logged in to display, otherwise redirects to the login page
    """

    template_name = 'accounts/profile.html'

    extra_context = {
        'page_title': 'Аккаунт',
    }

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class SettingsView(TemplateView):
    pass


class LoginView(TemplateView):
    """TemplateView for displaying login form page and login processing"""

    template_name = 'accounts/login.html'

    extra_context = {
        'page_title': 'Вход',
    }

    def get(self, request, *args, **kwargs):
        """GET request given: checks if the request.user was already logged in
        and returns login form page or redirects to the main page

        Also checks if there are errors during recent login attempt
        and pass them to the template context
        :param request: HttpRequest
        :return: HttpResponse
        """
        if request.user.is_anonymous:
            if kwargs.get('error'):
                self.extra_context['error'] = kwargs.get('error')
            else:
                try:
                    del self.extra_context['error']
                except KeyError:
                    pass

            return super().get(request, *args, **kwargs)
        else:
            return redirect('/')

    def post(self, request, *args, **kwargs):
        """POST request given: validates given email and password,
        authenticates the user, logs him in, creates a cart from anonymous cart
        if existing user cart is empty and redirects to the account profile page

        If validation failed then returns get() with error
        """
        if request.user.is_anonymous:
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not email:
                return self.get(request, error='Введите адрес электронной почты')

            if not password:
                return self.get(request, error='Введите пароль')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                anonymous_cart = request.session.get('cart', [])

                request.session.clear()

                if not Cart.objects.get_cart(user).get_items():
                    Cart.objects.create_from_anonymous(anonymous_cart, user)

                login(request, user)

                return redirect('/')
            else:
                return self.get(request, error='Адрес электронной почты или пароль неверны')
        else:
            return redirect('/accounts/profile/')


class LogoutView(View):
    """Logout view

    Logs the user out if he is logged in
    """
    def post(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            logout(request)

        return redirect('/')


class RegisterView(TemplateView):
    template_name = 'accounts/register.html'

    extra_context = {
        'page_title': 'Регистрация',
    }

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            if kwargs.get('error'):
                self.extra_context['error'] = kwargs.get('error')
            else:
                try:
                    del self.extra_context['error']
                except KeyError:
                    pass

            return super().get(request, *args, **kwargs)
        else:
            return redirect('/accounts/profile/')

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                validate_email(email)
            except ValidationError:
                return self.get(request, error='Введите корректный адрес электронной почты')

            if not password:
                return self.get(request, error='Введите пароль')

            try:
                user = User.objects.create_user(email=email, password=password)

                anonymous_cart = request.session.get('cart', [])

                login(request, user)

                return redirect('/')
            except IntegrityError:
                return self.get(request, error='Пользователь с введенным адресом электронной почты уже существует')
        else:
            return redirect('/accounts/profile/')


class RecoverView(TemplateView):
    template_name = 'accounts/recover.html'

    extra_context = {
        'page_title': 'Восстановление пароля',
    }

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            if kwargs.get('error'):
                self.extra_context['error'] = kwargs.get('error')
            else:
                try:
                    del self.extra_context['error']
                except KeyError:
                    pass

            return super().get(request, *args, **kwargs)
        else:
            return redirect('/accounts/profile/')

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            email = request.POST.get('email')

            if not email:
                return self.get(request, error='Введите корректный адрес электронной почты')
        else:
            return redirect('/accounts/profile/')
