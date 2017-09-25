from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from django.views import View
from edgecomics.config import SITE_ADDRESS
from previews.models import Monthly, Weekly
from previews.monthly_parser import MonthlyParser
from previews.weekly_parser import WeeklyParser
from previews.xls_generator import XLSGenerator
import json


class ParserView(View):
    method_list = [
        'parse',
        'postparse',
        'upload',
        'price',
    ]

    def get(self, request: HttpRequest, method: str = None) -> HttpResponse:
        if method is None:
            return render(request, 'previews/index.html')
        else:
            if hasattr(self, method):
                return getattr(self, method)(request)
            else:
                return HttpResponseBadRequest()

    def parse(self, request: HttpRequest) -> HttpResponse:
        try:
            parser = globals()[request.GET.get('mode').capitalize() + 'Parser'](request.GET.get('release_date', None))
        except KeyError:
            return HttpResponse(
                json.dumps({'error': 'wrong mode: %s' % request.GET.get('mode')}),
                content_type='application/json',
            )

        parser.parse()

        return HttpResponse(
            json.dumps({'entry_list': parser.parsed, 'session_timestamp': parser.session_timestamp}),
            content_type='application/json',
        )

    def postparse(self, request: HttpRequest) -> HttpResponse:
        mode = request.GET.get('mode')

        if mode is None:
            return HttpResponseBadRequest(json.dumps({'error': 'no mode specified'}), content_type='application/json')

        mode = mode.capitalize()

        parser = globals()[mode + 'Parser'].OneParser(globals()[mode].objects.get(id=request.GET.get('id')))

        parser.postload()
        cover_list = parser.download_covers()

        return HttpResponse(
            json.dumps({'cover': cover_list['thumb'],
                        'title': parser.model.title}, separators=[',', ':']),
            content_type='application/json'
        )

    def upload(self, request: HttpRequest) -> HttpResponse:
        pass

    def price(self, request: HttpRequest) -> HttpResponse:
        xls = XLSGenerator(request.GET.get('mode'), request.GET.get('session_timestamp'))

        path = xls.generate()

        return HttpResponse(json.dumps({'url': SITE_ADDRESS + path}), content_type='application/json')
