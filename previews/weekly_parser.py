from previews.models import Weekly, PUBLISHERS, PRICES
from previews.parser import Parser
from edgecomics.settings import MEDIA_ROOT
from edgecomics.config import SITE_ADDRESS
from commerce.models import DEFAULT_WEIGHT
import os.path
import datetime
import requests
from bs4 import BeautifulSoup
import demjson
import json


class WeeklyParser(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._convert_date()

    parse_url = 'http://midtowncomics.com/store/ajax_wr_online.asp'
    publishers = filter(lambda x: x.get('load_weekly'), PUBLISHERS)
    release_date_wdate = ''
    page = None
    soup = None
    cover_urls = [
        ('full', 'http://midtowncomics.com/images/product/xl/%s_xl.jpg'),
        ('thumb', 'http://midtowncomics.com/images/product/stnl/%s_sth.jpg'),
    ]

    model = Weekly

    def _convert_date(self):
        if isinstance(self.release_date, str):
            self.release_date = datetime.datetime.strptime(self.release_date, '%Y-%m-%d')

            if self.release_date.month > 2:
                month = self.release_date.month - 2
                year = self.release_date.year
            else:
                month = self.release_date.month + 10
                year = self.release_date.year - 1

            self.release_date_wdate = self.release_date.replace(year=year, month=month).strftime('%-m/%-d/%Y')

    @staticmethod
    def _convert_response(response):
        return demjson.decode(response)

    def _request_entries(self, publisher):
        raw = requests.get(self.parse_url, {'cat': publisher['midtown_code'], 'wdate': self.release_date_wdate}).text
        return WeeklyParser._convert_response(raw)

    def _date_from_soup(self):
        date_page = requests.get('http://midtowncomics.com/store/weeklyreleasebuy.asp')
        date_soup = BeautifulSoup(date_page.text, self.parse_engine)
        date_string = date_soup.find('option', {'selected': ''})['value']

        self.release_date = datetime.datetime.strptime(date_string, '%m/%d/%Y')
        self.release_date_wdate = date_string

    def _parse_by_publisher(self, publisher):
        entries = self._request_entries(publisher)

        for entry in entries:
            params = {
                'title': entry['pr_ttle'],
                'publisher': publisher['full_name'],
                'quantity': None,
                'diamond_id': None,
                'midtown_id': entry['pr_id'],
                'release_date': self.release_date,
            }

            price_origin = entry['pr_lprice']

            try:
                price_origin = float(price_origin)
            except ValueError:
                price_origin = 0.0

            params['price_origin'] = price_origin

            prices = PRICES['weekly'].get(price_origin, {})

            params['price'] = prices.get('price', 0.0)
            params['bought'] = prices.get('bought', 0.0)
            params['weight'] = prices.get('weight', DEFAULT_WEIGHT)
            params['discount'] = prices.get('discount', 0.0)

            cover_list = {}

            for url in self.cover_urls:
                if json.loads(entry['xl']) is True:
                    _url = url[1] % params['midtown_id']
                else:
                    _url = os.path.join(SITE_ADDRESS, 'media/previews/dummy.jpg')

                cover_list[url[0]] = _url

            model = self.model.objects.create(**params)
            model.cover_list = cover_list
            model.save()

            self.parsed.append(model.id)

    def parse(self):
        if self.release_date is None:
            self._date_from_soup()

        self._delete_old()

        for publisher in self.publishers:
            self._parse_by_publisher(publisher)

    class OneParser(Parser.OneParser):
        def __init__(self, model):
            super().__init__()

            self.model = model

        description_url = 'http://midtowncomics.com/store/dp.asp'

        def load_description(self):
            description_page = requests.get(self.description_url, {'PRID': self.model.midtown_id})
            description_soup = BeautifulSoup(description_page.text, self.parse_engine)

            self.model.description = description_soup.find('p', {'class': 'shorten'}).text

            diamond_container = description_soup.find('span', {'id': 'diamond_container'})

            if diamond_container is not None:
                self.model.diamond_id = diamond_container.text

            self.model.save()

            return self.model.description

        def download_covers(self):
            dummy_url = os.path.join(SITE_ADDRESS, 'media/previews/dummy.jpg')
            dirs_path = os.path.join(MEDIA_ROOT, 'previews')
            download_path = os.path.join(dirs_path, '%s/%s')
            downloaded_url = os.path.join(SITE_ADDRESS, 'media/previews/%s/%s')

            if isinstance(self.model.cover_list, str):
                self.model.cover_list = json.loads(self.model.cover_list)

            for item in self.model.cover_list.items():
                if item[1] != dummy_url:
                    filename = item[0] + '.jpg'

                    image_response = requests.get(item[1], stream=True)
                    image = image_response.raw.read()

                    model_covers_path = os.path.join(dirs_path, self.model.diamond_id)

                    if not os.path.exists(model_covers_path):
                        os.mkdir(model_covers_path)

                    out_file = open(download_path % (self.model.diamond_id, filename), 'wb')
                    out_file.write(image)
                    out_file.close()

                    self.model.cover_list[item[0]] = downloaded_url % (self.model.diamond_id, filename)

            self.model.save()

            return self.model.cover_list
