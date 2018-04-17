import json

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import render
from django.views import View
from edgecomics.config import SITE_ADDRESS, HAWK_TOKEN
from previews.models import Monthly, Weekly
from previews.parser import Parser
from previews.monthly_parser import MonthlyParser
from previews.weekly_parser import WeeklyParser
from previews.vk_uploader import VKUploader
from previews.xls_generator import XLSGenerator

from hawkcatcher import Hawk


class ParserView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hawk = Hawk(HAWK_TOKEN)

    def get(self, request, method=None):
        if method is None:
            return render(request, 'previews/index.html')
        else:
            if hasattr(self, method):
                try:
                    return getattr(self, method)(request)
                except SystemExit:
                    raise
                except:
                    self.hawk.catch()
                    return HttpResponseServerError()
            else:
                return HttpResponseBadRequest()

    def vk(self, request):
        return render(request, 'previews/vk.html', {'groups': VKUploader.list_groups(), 'dates': Parser.list_dates()})

    def parse(self, request):
        try:
            parser = globals()[request.GET.get('mode').capitalize() + 'Parser'](request.GET.get('release_date', None))
        except (KeyError, AttributeError):
            return HttpResponse(
                json.dumps({'error': 'wrong mode: %s' % request.GET.get('mode')}),
                content_type='application/json',
            )

        parser.parse()

        return HttpResponse(
            json.dumps({'entry_list': parser.parsed, 'session': parser.session}),
            content_type='application/json',
        )

    def postparse(self, request):
        mode = request.GET.get('mode')

        if mode is None:
            return HttpResponseBadRequest(
                json.dumps({'error': 'no mode specified'}),
                content_type='application/json',
            )

        if mode == 'monthly':
            dummy_specs = ('dummy_prwld.png', 120, 180)
        elif mode == 'weekly':
            dummy_specs = ('dummy_mdtwn.jpg', 300, 462)

        mode = mode.capitalize()

        glob_parser = globals()[mode + 'Parser']
        model = globals()[mode]

        parser = glob_parser.OneParser(
            model.objects.get(id=request.GET.get('id')),
            dummy_specs,
        )

        parser.postload()
        parser.store_cover()
        parser.capella.resize(120)
        thumb = parser.capella.get_url()

        return HttpResponse(
            json.dumps({
                'cover': thumb,
                'title': parser.model.title
            }, separators=[',', ':']),
            content_type='application/json',
        )

    def post(self, request):
        group_id = request.POST.get('group_id')

        if group_id is None:
            return HttpResponseBadRequest(
                json.dumps({'error': 'no group id specified'}),
                content_type='application/json',
            )

        session = request.POST.get('session')

        if session is None:
            return HttpResponseBadRequest(
                json.dumps({'error': 'no session specified'}),
                content_type='application/json',
            )

        uploader = VKUploader(group_id, session, options={'msg_link': request.POST.get('msg_link')})
        uploader.upload()

        return HttpResponse(json.dumps({'success': True}), content_type='application/json')

    def price(self, request):
        xls = XLSGenerator(
            request.GET.get('mode'),
            request.GET.get('session'),
            title_under_threshold='Предзаказы %s' if request.GET.get('mode') == 'weekly' else 'Синглы %s',
        )

        uri = xls.generate()

        return HttpResponse(json.dumps({'url': SITE_ADDRESS + uri}), content_type='application/json')
