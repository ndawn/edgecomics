import os
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
        print('release_date (raw):', release_date, '| release_date (converted):', self.release_date)
        self.session = int(time.time())
        print('session:', self.session)

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

    class OneParser:
        def __init__(self, model, vendor_dummy):
            self.model = model
            self.parse_engine = 'lxml'

            self.capella = Capella()

            self.dummy_url = os.path.join(SITE_ADDRESS, 'media/previews/dummy.jpg')
            self.vendor_dummy_path = os.path.join(MEDIA_ROOT, 'previews', vendor_dummy[0])
            self.vendor_dummy_width = vendor_dummy[1]

        dummy = 'https://capella.pics/47ffad88-8545-4c0c-8c7b-fe2c648e4024'
