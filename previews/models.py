from django.db import models
from commerce.models import Item, PriceMap


class Preview(Item):
    class Meta:
        verbose_name = 'Предзаказ'
        verbose_name_plural = 'Предзаказы'
    
    MODE_CHOICES = {
        'monthly': 'Месяц',
        'weekly': 'Неделя',
    }
    
    mode = models.CharField(
        null=True,
        max_length=8,
        choices=MODE_CHOICES.items(),
        verbose_name='Тип',
    )
    
    title_origin = models.CharField(
        default='Без названия',
        blank=True,
        max_length=512,
        verbose_name='Оригинальное название',
    )

    price_map = models.ForeignKey(
        PriceMap,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Таблица цен',
    )

    diamond_id = models.CharField(
        null=True,
        max_length=9,
        verbose_name='ID Diamond',
    )

    release_date = models.DateField(
        null=True,
        verbose_name='Дата выхода',
    )

    session = models.BigIntegerField(
        null=True,
        verbose_name='Сессия',
    )

    midtown_id = models.CharField(
        null=True,
        max_length=64,
        verbose_name='Код Midtown',
    )

    @staticmethod
    def list_dates():
        dates = []

        for preview in Preview.objects.distinct('session'):
            dates.append(Preview.mode_and_date_from_session(preview.session))

        return dates

    @staticmethod
    def mode_and_date_from_session(session):
        dates = [
            x['release_date']
            for x in Preview.objects.filter(session=session).distinct('release_date').values('release_date')
        ]
        dates = list(filter(lambda x: x is not None, dates))

        if len(dates) == 1:
            return {
                'mode': 'weekly',
                'release_date': dates[0],
                'session': session,
            }
        else:
            try:
                release_date = min(dates).replace(day=1),
            except ValueError:
                release_date = None

            return {
                'mode': 'monthly',
                'release_date': release_date,
                'session': session,
            }
