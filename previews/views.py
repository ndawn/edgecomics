import json

from django.http import JsonResponse
from django.views import View
from edgecomics.config import SITE_ADDRESS, HAWK_TOKEN
from previews.models import Preview
from previews.monthly_parser import MonthlyParser
from previews.weekly_parser import WeeklyParser
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
        return JsonResponse({})

    def post(self, request):
        mode = request.POST.get('mode')

        if mode == 'monthly':
            parser = MonthlyParser
        elif mode == 'weekly':
            parser = WeeklyParser
        else:
            return JsonResponse({'success': False, 'message': 'wrong mode: %s' % mode})

        parser = parser(request.GET.get('release_date'))

        parser.queue()

        return JsonResponse({'success': True, 'session': parser.session})

    def put(self, request):
        mode = request.GET.get('mode')

        if mode is None:
            return JsonResponse({'success': False, 'message': 'no mode specified'})

        if mode == 'monthly':
            parser = MonthlyParser
            dummy_specs = ('dummy_prwld.png', 120, 180)
        elif mode == 'weekly':
            parser = WeeklyParser
            dummy_specs = ('dummy_mdtwn.jpg', 300, 462)
        else:
            return JsonResponse({'success': False, 'message': 'wrong mode: %s' % request.GET.get('mode')})

        parser = parser.OneParser(
            Preview.objects.get(id=request.GET.get('id')),
            dummy_specs,
        )

        parser.postparse()
        parser.store_cover()
        parser.capella.resize(120)
        thumb = parser.capella.get_url()

        return JsonResponse({
            'success': True,
            'cover': thumb,
            'title': parser.instance.title
        })


@hawk_catch
class VKView(View):
    def get(self, request):
        return JsonResponse({'groups': VKUploader.list_groups(), 'dates': Preview.list_dates()})

    def post(self, request):
        group_id = request.POST.get('group_id')
        session = request.POST.get('session')

        if (group_id is None) or (session is None):
            return JsonResponse({'success': False, 'message': 'no group id or session specified'})

        uploader = VKUploader(group_id, session, options={'msg_link': request.POST.get('msg_link')})
        uploader.queue()

        return JsonResponse({'success': True})

    def put(self, request):
        try:
            cover = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'invalid request'})

        return JsonResponse({'success': True, **VKUploader.upload(cover)})


@hawk_catch
class PriceView(View):
    def get(self, request):
        return JsonResponse({'dates': Preview.list_dates()})

    def post(self, request):
        mode = request.GET.get('mode')

        xls = XLSGenerator(
            mode,
            request.GET.get('session'),
            title_under_threshold='Предзаказы %s' if mode == 'weekly' else 'Синглы %s',
        )

        uri = xls.generate()

        return JsonResponse({'success': True, 'url': SITE_ADDRESS + uri})
