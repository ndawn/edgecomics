import os.path
import locale
import datetime
import json
import re

from previews.models import Monthly, PRICES
from previews.parser import Parser
from edgecomics.settings import MEDIA_ROOT
from edgecomics.config import SITE_ADDRESS
from commerce.models import DEFAULT_WEIGHT, Publisher

from bs4 import BeautifulSoup
import titlecase
import requests
from pycapella import Capella


class MonthlyParser(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._set_date()

        locale.setlocale(locale.LC_TIME, 'en_GB.UTF-8')

    parse_url = 'https://previewsworld.com/catalog'
    publishers = Publisher.objects.all()
    release_date_batch = ''
    page = None
    soup = None
    cover_url = 'https://previewsworld.com/siteimage/catalogimage/%s?type=1'
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

    def _set_date(self):
        if self.release_date is not None:
            self.release_date = datetime.datetime.strptime(self.release_date, '%Y-%m-%d')
            self.release_date_batch = self.release_date.strftime('%b%y')

    def _delete_old(self):
        self.model.objects.filter(release_date__month=self.release_date.month).delete()  #TODO: rewrite

    def _make_soup(self):
        self.page = requests.get(self.parse_url, {'batch': self.release_date_batch})
        self.soup = BeautifulSoup(self.page.text, self.parse_engine)

    def _date_from_soup(self):
        if self.soup is not None:
            date_container = self.soup.find('div', {'class': 'catalogDisclaimer'})
            date_string = date_container.find_all('strong')[-1].text

            self.release_date = datetime.datetime.strptime(date_string, '%B %Y')
            self.release_date_batch = self.release_date.strftime('%b%y')
        else:
            raise ValueError('The soup is not yet cooked')

    def _parse_by_publisher(self, publisher):
        print(publisher)

        entries = self.soup.find('div', {'id': 'NewReleases_' + publisher.abbreviature}) \
                           .find_all('div', {'class': 'nrGalleryItem'})

        for entry in entries:
            params = {
                'title': self._process_title(entry.find('div', {'class': 'nrGalleryItemTitle'}).text.replace('\xa0', ' ')),
                'publisher': publisher,
                'quantity': None,
                'diamond_id': entry.find('div', {'class': 'nrGalleryItemDmdNo'}).text,
                'session': self.session,
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

            model = self.model.objects.create(**params)
            model.cover_url = self.cover_url % cover_name
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
        description_url = 'https://previewsworld.com/catalog/%s'

        def postload(self):
            description_page = requests.get(self.description_url % self.model.diamond_id)
            description_soup = BeautifulSoup(description_page.text, self.parse_engine)

            text_container = description_soup.find('div', {'class': 'Text'})

            if text_container is not None:
                try:
                    text_container.find('div', {'class': 'ItemCode'}).decompose()
                except AttributeError:
                    pass

                try:
                    text_container.find('div', {'class': 'Creators'}).decompose()
                except AttributeError:
                    pass

                try:
                    text_container.find('div', {'class': 'SRP'}).decompose()
                except AttributeError:
                    pass

                try:
                    release_date = text_container.find('div', {'class': 'ReleaseDate'}).extract().text.strip()
                except AttributeError:
                    release_date = None

                try:
                    self.model.release_date = datetime.datetime.strptime(release_date, 'In Shops: %b %d, %Y')
                except (ValueError, AttributeError):
                    self.model.release_date = None

                self.model.description = text_container.text.strip()

                self.model.save()

            return self.model.description

        def is_dummy(self, url):
            temp_path = os.path.join(MEDIA_ROOT, 'previews/temp')

            temp = open(temp_path, 'wb')
            print(url)
            temp.write(requests.get(url).content)
            temp.close()

            temp = open(temp_path, 'rb')
            dummy = open(self.vendor_dummy_path, 'rb')

            res = temp.read() == dummy.read()

            temp.close()
            dummy.close()

            return res

        def store_cover(self):
            response = self.capella.upload_url(self.model.cover_url)

            if response['success']:
                print(response)
                self.capella.resize(self.vendor_dummy_width, self.vendor_dummy_height)

                if self.is_dummy(self.capella.get_url()):
                    self.model.cover_url = self.dummy
                else:
                    self.model.cover_url = response['url']

                self.model.save()
