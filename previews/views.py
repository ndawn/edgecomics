import json

from django.http import JsonResponse, HttpResponseServerError
from django.views import View
from django.views.decorators.csrf import get_token
from util.queues import Consumer
from edgecomics.config import SITE_ADDRESS, HAWK_TOKEN
from previews.models import Preview
from previews.monthly_parser import MonthlyParser, SingleItemParser as SingleMonthlyItemParser
from previews.weekly_parser import WeeklyParser, SingleItemParser as SingleWeeklyItemParser
from previews.vk_uploader import VKUploader
from previews.xls_generator import XLSGenerator

from hawkcatcher import Hawk


hawk = Hawk(HAWK_TOKEN)


def hawk_catch(cls):
    def catch(f):
        def _catch(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except SystemExit:
                raise
            except:
                hawk.catch()
                return HttpResponseServerError()

        return _catch

    for attr in cls.__dict__:
        fn = getattr(cls, attr)

        if callable(fn) and hasattr(fn, '__name__'):
            if fn.__name__ in ('get', 'post', 'put', 'patch', 'update', 'delete', 'head', 'options'):
                setattr(cls, attr, catch(fn))
    return cls


@hawk_catch
class ParseView(View):
    def get(self, request):
        if not request.path.endswith('/next/'):
            return JsonResponse({'csrfmiddlewaretoken': get_token(request)})
        else:
            mode = request.GET.get('mode')

            if mode is None:
                return JsonResponse({'success': False, 'message': 'no mode specified'})

            if mode == 'monthly':
                parser = SingleMonthlyItemParser
            elif mode == 'weekly':
                parser = SingleWeeklyItemParser
            else:
                return JsonResponse({'success': False, 'message': 'wrong mode: %s' % request.GET.get('mode')})

            consumed = Consumer('parse').get()

            if consumed is not None:
                parser = parser(
                    Preview.objects.get(
                        pk=consumed['preview_id']
                    )
                )
            else:
                return JsonResponse({
                    'success': True,
                    'cover': None,
                    'title': None,
                })

            parser.postparse()
            cover = parser.store_cover()

            return JsonResponse({
                'success': True,
                'cover': cover,
                'title': parser.instance.title,
            })

    def post(self, request):
        mode = request.POST.get('mode')

        if mode == 'monthly':
            parser = MonthlyParser
        elif mode == 'weekly':
            parser = WeeklyParser
        else:
            return JsonResponse({'success': False, 'message': 'wrong mode: %s' % mode})

        parser = parser(request.POST.get('release_date'))

        preview_count = parser.queue()

        return JsonResponse({'success': True, 'session': parser.session, 'count': preview_count})


@hawk_catch
class VKView(View):
    def get(self, request):
        return JsonResponse({
            'groups': VKUploader.list_groups(),
            'dates': Preview.list_dates(),
            'csrfmiddlewaretoken': get_token(request),
        })

    def post(self, request):
        group_id = request.POST.get('group_id')
        session = request.POST.get('session')

        if (group_id is None) or (session is None):
            return JsonResponse({'success': False, 'message': 'no group id or session specified'})

        uploader = VKUploader(group_id, session, options={'msg_link': request.POST.get('msg_link')})
        preview_count = uploader.queue()

        return JsonResponse({'success': True, 'count': preview_count})

    def put(self, request):
        try:
            cover = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'invalid request'})

        return JsonResponse({'success': True, **VKUploader.upload(cover)})


@hawk_catch
class PriceView(View):
    def get(self, request):
        return JsonResponse({
            'dates': Preview.list_dates(),
            'csrfmiddlewaretoken': get_token(request),
        })

    def post(self, request):
        mode = request.POST.get('mode')

        xls = XLSGenerator(
            mode,
            request.POST.get('session'),
            title_under_threshold='Предзаказы %s' if mode == 'weekly' else 'Синглы %s',
        )

        uri = xls.generate()

        return JsonResponse({'success': True, 'url': SITE_ADDRESS + uri})
