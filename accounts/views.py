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


