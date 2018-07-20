from django.views.decorators.csrf import get_token
from django.http import JsonResponse
from django.views import View
from util.queues import Consumer


class ParseView(View):
    def get(self, request):
        consumed = Consumer('parse').get()

        if consumed is not None:
            consumed = {
                **consumed,
                'csrfmiddlewaretoken': get_token(request),
            }

        return JsonResponse(consumed, safe=False)


class VKView(View):
    def get(self, request):
        return JsonResponse(Consumer('vk').get(), safe=False)
