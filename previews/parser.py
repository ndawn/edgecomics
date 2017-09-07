from previews.models import Preview
from typing import Union
import datetime


class Parser:
    def __init__(self, release_date: Union[None, str, datetime.date] = None) -> None:
        self.release_date = release_date

    parse_url = ''

    cover_urls = {}

    parsed = []

    def parse(self):
        pass

    class OneParser:
        pass
