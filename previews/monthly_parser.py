from previews.models import Monthly, PUBLISHERS, PRICES
from previews.parser import Parser
from edgecomics.settings import MEDIA_ROOT
from edgecomics.config import SITE_ADDRESS
from bs4 import BeautifulSoup
from commerce.models import DEFAULT_WEIGHT
import titlecase
import os.path
import datetime
import time
import requests
import json
import re


class MonthlyParser(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._convert_date()

    parse_url = 'https://previewsworld.com/catalog'
    publishers = PUBLISHERS
    release_date_batch = ''
    session_timestamp = time.time()
    page = None
    soup = None
    cover_urls = {
        'full': 'https://previewsworld.com/siteimage/catalogimage/%s?type=1',
        'thumb': 'https://previewsworld.com/siteimage/catalogthumbnail/%s?type=1',
    }
    model = Monthly

    def _process_title(self, title):
        def abbrs(word, **kwargs):
            if word in ('TP', 'HC'):
                return word

        string = titlecase.titlecase(title, callback=abbrs) \
            .replace('Var Ed', 'Variant') \
            .replace('Var ', 'Variant ') \
            .replace('Leg', '')

        return ' '.join(re.sub('\(.*\)', '', string).split())

    def _convert_date(self):
        if isinstance(self.release_date, str):
            self.release_date = datetime.datetime.strptime(self.release_date, '%Y-%m-%d')

            if self.release_date.month > 2:
                month = self.release_date.month - 2
                year = self.release_date.year
            else:
                month = self.release_date.month + 10
                year = self.release_date.year - 1

            self.release_date_batch = self.release_date.replace(year=year, month=month).strftime('%b%y')

    def _delete_old(self):
        self.model.objects.filter(release_date__month=self.release_date.month).delete()

    def _make_soup(self):
        self.page = requests.get(self.parse_url, {'batch': self.release_date_batch})
        self.soup = BeautifulSoup(self.page.text, self.parse_engine)

    def _date_from_soup(self):
        if self.soup is not None:
            date_container = self.soup.find('div', {'class': 'catalogDisclaimer'})
            date_string = date_container.find_all('strong')[-1].text

            self.release_date = datetime.datetime.strptime(date_string, '%B %Y')
        else:
            raise ValueError('The soup is not yet cooked')

    def _parse_by_publisher(self, publisher):
        entries = self.soup.find('div', {'id': 'NewReleases_' + publisher['abbr']}) \
                           .find_all('div', {'class': 'nrGalleryItem'})

        for entry in entries:
            params = {
                'title': self._process_title(entry.find('div', {'class': 'nrGalleryItemTitle'}).text.replace('\xa0', ' ')),
                'publisher': publisher['full_name'],
                'quantity': None,
                'diamond_id': entry.find('div', {'class': 'nrGalleryItemDmdNo'}).text,
                'session_timestamp': self.session_timestamp,
            }

            price_origin = entry.find('div', {'class': 'nrGalleryItemSRP'}).text.lstrip('$')

            try:
                price_origin = float(price_origin)
            except ValueError:
                price_origin = 0.0

            params['price_origin'] = price_origin

            prices = PRICES['monthly'].get(price_origin, {})

            params['price'] = prices.get('price', 0.0)
            params['bought'] = prices.get('bought', 0.0)
            params['weight'] = prices.get('weight', DEFAULT_WEIGHT)
            params['discount'] = prices.get('discount', 0.0)
            params['discount_superior'] = prices.get('discount_superior', 0.0)

            cover_element = entry.find('div', {'class': 'nrGalleryItemImage'}).a.img
            cover_name = os.path.basename(cover_element.get('data-src', cover_element.get('src')))
            cover_list = {k: v % cover_name for (k, v) in self.cover_urls.items()}

            model = self.model.objects.create(**params)
            model.cover_list = cover_list
            model.save()

            self.parsed.append(model.id)

    def parse(self):
        self._make_soup()

        if self.release_date is None:
            self._date_from_soup()

        self._delete_old()

        for publisher in self.publishers:
            self._parse_by_publisher(publisher)

    class OneParser(Parser.OneParser):
        def __init__(self, model):
            super().__init__()

            self.model = model

        description_url = 'https://previewsworld.com/catalog/%s'

        def postload(self):
            description_page = requests.get(self.description_url % self.model.diamond_id)
            description_soup = BeautifulSoup(description_page.text, self.parse_engine)

            text_container = description_soup.find('div', {'class': 'Text'})

            if text_container is not None:
                text_container.find('div', {'class': 'ItemCode'}).decompose()
                text_container.find('div', {'class': 'Creators'}).decompose()
                text_container.find('div', {'class': 'SRP'}).decompose()

                release_date = text_container.find('div', {'class': 'ReleaseDate'}).extract().text.strip()

                try:
                    self.model.release_date = datetime.datetime.strptime(release_date, 'In Shops: %b %d, %Y')
                except ValueError:
                    self.model.release_date = None

                self.model.description = text_container.text.strip()

                self.model.save()

            return self.model.description

        def download_covers(self):
            dummy_url = os.path.join(SITE_ADDRESS, 'media/previews/dummy.jpg')
            dummy_cover = open(os.path.join(MEDIA_ROOT, 'previews/dummy_prwld.png'), 'rb')
            dirs_path = os.path.join(MEDIA_ROOT, 'previews')
            download_path = os.path.join(dirs_path, '%s/%s')
            downloaded_url = os.path.join(SITE_ADDRESS, 'media/previews/%s/%s')

            if isinstance(self.model.cover_list, str):
                self.model.cover_list = json.loads(self.model.cover_list)

            for item in self.model.cover_list.items():
                filename = item[0] + '.jpg'

                image_response = requests.get(item[1], stream=True)
                image = image_response.raw.read()

                if image != dummy_cover.read():
                    model_covers_path = os.path.join(dirs_path, self.model.diamond_id)

                    if not os.path.exists(model_covers_path):
                        os.mkdir(model_covers_path)

                    out_file = open(download_path % (self.model.diamond_id, filename), 'wb')
                    out_file.write(image)
                    out_file.close()

                    self.model.cover_list[item[0]] = downloaded_url % (self.model.diamond_id, filename)
                else:
                    self.model.cover_list[item[0]] = dummy_url

            self.model.save()

            return self.model.cover_list
