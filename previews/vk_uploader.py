import os.path
import locale
import time

from edgecomics.settings import MEDIA_ROOT
from edgecomics.config import VK_ACCESS_TOKEN, VK_API_VERSION
from previews.models import Preview
from util.queues import Producer
from commerce.models import Publisher

import requests
import vk


class VKUploader:
    def __init__(self, group_id, session, options=None):
        self.group_id = group_id
        self.session = session
        self.api = VKUploader.api()
        self.producer = Producer('vk')

        if options is not None and options.get('msg_link'):
            self.msg_link = options.get('msg_link')
        else:
            self.msg_link = 'https://vk.me/-%s' % group_id

        mode_and_date = Preview.mode_and_date_from_session(session)

        self.mode = mode_and_date['mode']
        self.release_date = mode_and_date['release_date']
        if isinstance(self.release_date, tuple):
            self.release_date = self.release_date[0]

    local_path = os.path.join(MEDIA_ROOT, 'previews')

    @staticmethod
    def api():
        session = vk.Session(VK_ACCESS_TOKEN)
        return vk.API(session, v=VK_API_VERSION)

    @staticmethod
    def list_groups():
        return VKUploader.api().groups.get(filter='admin', extended=1)['items']

    def queue(self):
        preview_count = 0

        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

        for publisher in Publisher.objects.all():
            time.sleep(0.35)

            def correct(d):
                return d + 'а' if d.endswith('т') else d[:-1] + 'я'

            if self.mode == 'monthly':
                album_date = self.release_date.strftime('%B')
            else:
                album_date = self.release_date.strftime('%d ') + correct(self.release_date.strftime('%B').lower())

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
                caption = '%s – %d рублей\nДата выхода: %s\nДля покупки писать: %s' % (
                    preview.title,
                    preview.price_map.discount,
                    preview.release_date.strftime('%-d ') + correct(preview.release_date.strftime('%B').lower()),
                    self.msg_link,
                )

                self.producer.send({
                    'id': preview.id,
                    'cover': {
                        'group_id': self.group_id,
                        'upload_url': upload_server['upload_url'],
                        'caption': caption,
                    },
                    'title': preview.title,
                })

                preview_count += 1

        locale.setlocale(locale.LC_TIME, '')

        return preview_count

    @staticmethod
    def upload(cover):
        preview = Preview.objects.get(id=cover['preview_id'])

        file_path = os.path.join(VKUploader.local_path, 'file0.png')

        file = open(file_path, 'wb')
        file.write(requests.get(preview.cover['lg']).content)
        file.close()

        file = open(file_path, 'rb')
        upload_status = requests.post(cover['upload_url'], files={'file1': file}).json()

        photo = VKUploader.api().photos.save(
            album_id=upload_status['aid'],
            group_id=cover['group_id'],
            server=upload_status['server'],
            photos_list=upload_status['photos_list'],
            hash=upload_status['hash'],
            caption=cover['caption'],
        )

        return {
            'success': True,
            'photo': photo,
            'title': preview.title,
        }
