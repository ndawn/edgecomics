from django.views import View
from django.http import JsonResponse

import cloudinary.api


class UsageView(View):
    def get(self, request):
        return JsonResponse(cloudinary.api.usage())


class PingView(View):
    def get(self, request):
        return JsonResponse(cloudinary.api.ping())
