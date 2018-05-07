from django.db import models
from commerce.models import Item, PriceMap


PRICES = {
    'monthly': {
        1: {
            'bought': 96,
            'superior': 150,
            'discount': 190,
            'default': 250,
            'weight': 100,
        },
        2.99: {
            'bought': 167.4,
            'superior': 230,
            'discount': 290,
            'default': 400,
            'weight': 100,
        },
        3.99: {
            'bought': 203.4,
            'superior': 290,
            'discount': 350,
            'default': 450,
            'weight': 100,
        },
        4.69: {
            'bought': 228.6,
            'superior': 330,
            'discount': 390,
            'default': 500,
            'weight': 100,
        },
        4.99: {
            'bought': 239.4,
            'superior': 330,
            'discount': 390,
            'default': 500,
            'weight': 100,
        },
        5.99: {
            'bought': 275.4,
            'superior': 390,
            'discount': 450,
            'default': 550,
            'weight': 100,
        },
        6.99: {
            'bought': 311.4,
            'superior': 430,
            'discount': 490,
            'default': 600,
            'weight': 100,
        },
        9.99: {
            'bought': 483,
            'superior': 590,
            'discount': 650,
            'default': 800,
            'weight': 700,
        },
        12.99: {
            'bought': 576,
            'superior': 690,
            'discount': 790,
            'default': 1100,
            'weight': 700,
        },
        14.99: {
            'bought': 663,
            'superior': 750,
            'discount': 850,
            'default': 1250,
            'weight': 700,
        },
        15.99: {
            'bought': 694,
            'superior': 790,
            'discount': 890,
            'default': 1300,
            'weight': 700,
        },
        16.99: {
            'bought': 750,
            'superior': 890,
            'discount': 990,
            'default': 1300,
            'weight': 700,
        },
        17.99: {
            'bought': 806,
            'superior': 990,
            'discount': 1090,
            'default': 1400,
            'weight': 700,
        },
        19.99: {
            'bought': 942,
            'superior': 1190,
            'discount': 1290,
            'default': 1600,
            'weight': 700,
        },
        24.99: {
            'bought': 1097,
            'superior': 1290,
            'discount': 1390,
            'default': 1700,
            'weight': 1000,
        },
        29.99: {
            'bought': 1277,
            'superior': 1590,
            'discount': 1690,
            'default': 1900,
            'weight': 1500,
        },
        34.99: {
            'bought': 1457,
            'superior': 1690,
            'discount': 1890,
            'default': 2200,
            'weight': 1900,
        },
        39.99: {
            'bought': 1736,
            'superior': 1990,
            'discount': 2190,
            'default': 2600,
            'weight': 1900,
        },
        49.99: {
            'bought': 2046,
            'superior': 2490,
            'discount': 2690,
            'default': 3500,
            'weight': 1900,
        },
        50: {
            'bought': 2046,
            'superior': 2490,
            'discount': 2690,
            'default': 3500,
            'weight': 1900,
        },
        75: {
            'bought': 2895,
            'superior': 3290,
            'discount': 3690,
            'default': 5000,
            'weight': 2000,
        },
        99.99: {
            'bought': 4340,
            'superior': 4990,
            'discount': 5490,
            'default': 7000,
            'weight': 3000,
        },
        100: {
            'bought': 4340,
            'superior': 4990,
            'discount': 5490,
            'default': 7000,
            'weight': 3000,
        },
        125: {
            'bought': 5611,
            'superior': 6290,
            'discount': 6690,
            'default': 8000,
            'weight': 3000,
        },
    },
    'weekly': {
        1: {
            'bought': 124,
            'discount': 239,
            'default': 300,
            'weight': 100,
        },
        2.54: {
            'bought': 219,
            'discount': 339,
            'default': 339,
            'weight': 100,
        },
        2.99: {
            'bought': 247,
            'discount': 389,
            'default': 500,
            'weight': 100,
        },
        3.39: {
            'bought': 272,
            'discount': 389,
            'default': 500,
            'weight': 100,
        },
        3.99: {
            'bought': 309,
            'discount': 439,
            'default': 550,
            'weight': 100,
        },
        4.24: {
            'bought': 325,
            'discount': 439,
            'default': 550,
            'weight': 100,
        },
        4.25: {
            'bought': 326,
            'discount': 439,
            'default': 550,
            'weight': 100,
        },
        5.09: {
            'bought': 378,
            'discount': 489,
            'default': 550,
            'weight': 100,
        },
        5.94: {
            'bought': 430,
            'discount': 549,
            'default': 650,
            'weight': 100,
        },
        5.95: {
            'bought': 431,
            'discount': 549,
            'default': 650,
            'weight': 100,
        },
        6.79: {
            'bought': 483,
            'discount': 639,
            'default': 750,
            'weight': 100,
        },
        8.49: {
            'bought': 588,
            'discount': 739,
            'default': 900,
            'weight': 200,
        },
        8.5: {
            'bought': 589,
            'discount': 739,
            'default': 900,
            'weight': 100,
        },
        10: {
            'bought': 682,
            'discount': 839,
            'default': 1000,
            'weight': 100,
        },
        10.2: {
            'bought': 694,
            'discount': 839,
            'default': 1000,
            'weight': 100,
        },
        12: {
            'bought': 806,
            'discount': 999,
            'default': 1300,
            'weight': 100,
        },
        12.75: {
            'bought': 853,
            'discount': 999,
            'default': 1300,
            'weight': 100,
        },
        15.3: {
            'bought': 1011,
            'discount': 1159,
            'default': 1400,
            'weight': 100,
        },
        17: {
            'bought': 1116,
            'discount': 1299,
            'default': 1500,
            'weight': 100,
        },
        18: {
            'bought': 1178,
            'discount': 1399,
            'default': 1600,
            'weight': 100,
        },
        21.25: {
            'bought': 1380,
            'discount': 1599,
            'default': 1800,
            'weight': 100,
        },
        25.5: {
            'bought': 1643,
            'discount': 1839,
            'default': 2000,
            'weight': 100,
        },
        29.75: {
            'bought': 1907,
            'discount': 2099,
            'default': 2500,
            'weight': 100,
        },
        11.04: {
            'bought': 576,
            'discount': 859,
            'default': 1100,
            'weight': 700,
        },
        12.74: {
            'bought': 663,
            'discount': 959,
            'default': 1250,
            'weight': 700,
        },
        13.59: {
            'bought': 694,
            'discount': 999,
            'default': 1300,
            'weight': 700,
        },
        14.44: {
            'bought': 750,
            'discount': 1099,
            'default': 1300,
            'weight': 700,
        },
        15.29: {
            'bought': 806,
            'discount': 1199,
            'default': 1400,
            'weight': 700,
        },
        16.99: {
            'bought': 942,
            'discount': 1399,
            'default': 1600,
            'weight': 700,
        },
        21.24: {
            'bought': 1097,
            'discount': 1499,
            'default': 1700,
            'weight': 1000,
        },
        25.49: {
            'bought': 1277,
            'discount': 1799,
            'default': 1900,
            'weight': 1500,
        },
        29.74: {
            'bought': 1457,
            'discount': 1999,
            'default': 2200,
            'weight': 1900,
        },
        33.99: {
            'bought': 1736,
            'discount': 2399,
            'default': 2600,
            'weight': 1900,
        },
        42.49: {
            'bought': 2046,
            'discount': 2899,
            'default': 3500,
            'weight': 1900,
        },
        42.5: {
            'bought': 2046,
            'discount': 2899,
            'default': 3500,
            'weight': 1900,
        },
        63.75: {
            'bought': 2895,
            'discount': 3899,
            'default': 5000,
            'weight': 2000,
        },
        84.99: {
            'bought': 4340,
            'discount': 5699,
            'default': 7000,
            'weight': 3000,
        },
        85: {
            'bought': 4340,
            'discount': 5699,
            'default': 7000,
            'weight': 3000,
        },
        106.25: {
            'bought': 5611,
            'discount': 6999,
            'default': 8000,
            'weight': 3000,
        },
    },
}


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
