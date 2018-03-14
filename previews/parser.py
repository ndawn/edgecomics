from previews.models import Preview
import datetime
import time


class Parser:
    def __init__(self, release_date=None):
        self.release_date = datetime.datetime.strptime(release_date, '%Y-%m-%d') if release_date is not None else None
        print('release_date (raw):', release_date, '| release_date (converted):', self.release_date)
        self.session_timestamp = int(time.time())
        print('session_timestamp:', self.session_timestamp)

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
        parse_engine = 'lxml'
