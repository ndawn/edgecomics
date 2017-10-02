from previews.models import Preview
from typing import Union
import datetime


class Parser:
    def __init__(self, release_date: Union[None, str] = None) -> None:
        self.release_date = release_date

    parse_url = ''
    parse_engine = 'lxml'

    cover_urls = {}

    parsed = []

    model = Preview

    def _date_from_soup(self):
        pass

    def _delete_old(self):
        self.model.objects.filter(release_date=self.release_date).delete()

    def parse(self):
        pass

    class OneParser:
        parse_engine = 'lxml'
