import os
import locale
import datetime
import time
import requests

from previews.models import Preview
from edgecomics.config import SITE_ADDRESS
from edgecomics.settings import MEDIA_ROOT

from pycapella import Capella


class Parser:
    def __init__(self, release_date=None):
        self.release_date = datetime.datetime.strptime(release_date, '%Y-%m-%d') if release_date is not None else None
        self.session = int(time.time())

    def __del__(self):
        locale.setlocale(locale.LC_TIME, '')

    parse_url = ''
    parse_engine = 'lxml'

    cover_urls = {}

    parsed = []

    model = Preview

    def _process_title(self, title):
        pass

    def _date_from_soup(self):
        pass

    def _delete_old(self):
        self.model.objects.filter(release_date=self.release_date).delete()

    def parse(self):
        pass

    @staticmethod
    def list_dates():
        dates = []

        for preview in Preview.objects.distinct('session'):
            dates.append(Parser.mode_and_date_from_session(preview.session))

        return dates

    @staticmethod
    def mode_and_date_from_session(session):
        dates = [
            x['release_date']
            for x in Preview.objects.filter(session=session).distinct('release_date').values('release_date')
        ]
        dates = list(filter(lambda x: x is not None, dates))

        if len(dates) == 1:
            return {
                'mode': 'weekly',
                'release_date': dates['release_date'] if isinstance(dates, datetime.date) else dates[0]['release_date'],
                'session': session,
            }
        else:
            try:
                release_date = min(dates).replace(day=1),
            except ValueError:
                release_date = None

            return {
                'mode': 'monthly',
                'release_date': release_date,
                'session': session,
            }


    class OneParser:
        def __init__(self, model, vendor_dummy):
            self.model = model
            self.parse_engine = 'lxml'

            self.capella = Capella()

            self.dummy_url = os.path.join(SITE_ADDRESS, 'media/previews/dummy.jpg')
            self.vendor_dummy_path = os.path.join(MEDIA_ROOT, 'previews', vendor_dummy[0])
            self.vendor_dummy_width = vendor_dummy[1]
            self.vendor_dummy_height = vendor_dummy[2]

        dummy = 'https://capella.pics/47ffad88-8545-4c0c-8c7b-fe2c648e4024'
