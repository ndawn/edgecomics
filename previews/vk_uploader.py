import os.path
import locale
import time

from edgecomics.settings import MEDIA_ROOT
from edgecomics.config import VK_ACCESS_TOKEN, VK_API_VERSION
#from edgecomics.queues import Sender
from previews.parser import Parser
from previews.models import Preview
from commerce.models import Publisher

import requests
import vk


class VKUploader:
    def __init__(self, group_id, session, options=None):
        self.group_id = group_id
        self.session = session
        self.api = VKUploader.api()
        self.local_path = os.path.join(MEDIA_ROOT, 'previews')

        if options is not None:
            self.msg_link = options.get('msg_link', 'https://vk.me/-%s' % group_id)
        else:
            self.msg_link = 'https://vk.me/-%s' % group_id

        mode_and_date = Parser.mode_and_date_from_session(session)

        self.mode = mode_and_date['mode']
        self.release_date = mode_and_date['release_date']
        if isinstance(self.release_date, tuple):
            self.release_date = self.release_date[0]

    @staticmethod
    def api():
        session = vk.Session(VK_ACCESS_TOKEN)
        return vk.API(session, v=VK_API_VERSION)

    @staticmethod
    def list_groups():
        return VKUploader.api().groups.get(filter='admin', extended=1)['items']

    def upload(self):
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

        #sender = Sender('vk')

        for publisher in Publisher.objects.all():
            correct = lambda d: d + 'а' if d.endswith('т') else d[:-1] + 'я'

            if self.mode == 'monthly':
                album_date = self.release_date.strftime('%B')
            else:
                album_date = self.release_date.strftime('%d ') + correct(self.release_date.strftime('%B').lower())

            time.sleep(1)

            album = self.api.photos.createAlbum(
                title='Предзаказы %s %s' % (publisher.short_name, album_date),
                group_id=self.group_id,
                upload_by_admins_only=1,
            )

            upload_server = self.api.photos.getUploadServer(
                album_id=album['id'],
                group_id=self.group_id,
            )

            previews = Preview.objects.filter(session=self.session, publisher=publisher)

            for preview in previews:
                file_path = os.path.join(self.local_path, 'file0.jpg')

                file = open(file_path, 'wb')
                file.write(requests.get(os.path.join(preview.cover_url, 'resize/400')).content)
                file.close()

                file = open(file_path, 'rb')
                upload_status = requests.post(upload_server['upload_url'], files={'file1': file}).json()

                print(upload_status)

                caption = '\n'.join([
                    preview.title + ' – ' + str(int(preview.discount * preview.price)) + ' рублей',
                    'Дата выхода: ' + preview.release_date.strftime('%-d ') + correct(preview.release_date.strftime('%B').lower()),
                    'Для покупки писать: ' + self.msg_link,
                ])

                photo = self.api.photos.save(
                    album_id=album['id'],
                    group_id=self.group_id,
                    server=upload_status['server'],
                    photos_list=upload_status['photos_list'],
                    hash=upload_status['hash'],
                    caption=caption,
                )

                print(photo)

                #sender.send({'success': True, 'cover': photo['photo_130'], 'title': preview.title})

        locale.setlocale(locale.LC_TIME, '')
