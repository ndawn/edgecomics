import locale
import datetime
import time

from previews.models import Preview
from edgecomics import config
from edgecomics.settings import MEDIA_ROOT
from util.queues import Producer

import cloudinary.api
import cloudinary.uploader


class Parser:
    def __init__(self, release_date=None):
        self.release_date = datetime.datetime.strptime(release_date, '%Y-%m-%d') if release_date is not None else None
        self.session = int(time.time())
        self.count = 0

        self.producer = Producer('parse')

        self._set_date()

    def __del__(self):
        locale.setlocale(locale.LC_TIME, '')

    publishers = None
    parse_url = ''
    parse_engine = 'lxml'

    cover_urls = {}

    def _set_date(self):
        pass

    def _process_title(self, title):
        pass

    def _date_from_soup(self):
        pass

    def _delete_old(self):
        Preview.objects.filter(release_date=self.release_date).delete()

    def _parse_by_publisher(self, publisher):
        pass

    def queue(self):
        if self.release_date is None:
            self._date_from_soup()

        self._delete_old()

        for publisher in self.publishers:
            self._parse_by_publisher(publisher)

        return self.count


class SingleItemParser:
    def __init__(self, instance):
        self.instance = instance
        self.parse_engine = 'lxml'

    dummy_vendor = ''

    def store_cover(self):
        try:
            image_data = cloudinary.uploader.upload(
                self.instance.cover_origin,
                folder='cover',
                phash=True,
                config=config.CLOUDINARY_CONFIG,
            )

            phash_distance = int(image_data['phash'], base=16) ^ int(config.DUMMY[self.dummy_vendor]['phash'], base=16)
            phash_identity = 1 - bin(phash_distance).count('1') / 64

            print()
            print('phash_identity:', phash_identity)

            if phash_identity > 0.98:
                cloudinary.uploader.destroy(image_data['public_id'], config=config.CLOUDINARY_CONFIG)
                self.instance.cover = None
            else:
                self.instance.cover = image_data['public_id']
        except cloudinary.api.Error:
            self.instance.cover = config.DUMMY['edge']['id']

        self.instance.save()

        print(self.instance.cover)

        return self.instance.cover
