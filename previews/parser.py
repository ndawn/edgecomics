from previews.models import Preview
from typing import Union
import time


class Parser:
    def __init__(self, release_date: Union[None, str] = None) -> None:
        self.release_date = release_date
        self.session_timestamp = int(time.time())

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
