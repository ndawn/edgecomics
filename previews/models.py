from django.db import models
from commerce.models import Item


PRICES = {
    'monthly': {
        1: {
            'bought': 96,
            'discount_superior': 150 / 250,
            'discount': 190 / 250,
            'price': 250,
            'weight': 100,
        },
        2.99: {
            'bought': 167.4,
            'discount_superior': 230 / 400,
            'discount': 290 / 400,
            'price': 400,
            'weight': 100,
        },
        3.99: {
            'bought': 203.4,
            'discount_superior': 290 / 450,
            'discount': 350 / 450,
            'price': 450,
            'weight': 100,
        },
        4.69: {
            'bought': 228.6,
            'discount_superior': 330 / 500,
            'discount': 390 / 500,
            'price': 500,
            'weight': 100,
        },
        4.99: {
            'bought': 239.4,
            'discount_superior': 330 / 500,
            'discount': 390 / 500,
            'price': 500,
            'weight': 100,
        },
        5.99: {
            'bought': 275.4,
            'discount_superior': 390 / 550,
            'discount': 450 / 550,
            'price': 550,
            'weight': 100,
        },
        6.99: {
            'bought': 311.4,
            'discount_superior': 430 / 600,
            'discount': 490 / 600,
            'price': 600,
            'weight': 100,
        },
        9.99: {
            'bought': 483,
            'discount_superior': 590 / 800,
            'discount': 650 / 800,
            'price': 800,
            'weight': 700,
        },
        12.99: {
            'bought': 576,
            'discount_superior': 690 / 1100,
            'discount': 790 / 1100,
            'price': 1100,
            'weight': 700,
        },
        14.99: {
            'bought': 663,
            'discount_superior': 750 / 1250,
            'discount': 850 / 1250,
            'price': 1250,
            'weight': 700,
        },
        15.99: {
            'bought': 694,
            'discount_superior': 790 / 1300,
            'discount': 890 / 1300,
            'price': 1300,
            'weight': 700,
        },
        16.99: {
            'bought': 750,
            'discount_superior': 890 / 1300,
            'discount': 990 / 1300,
            'price': 1300,
            'weight': 700,
        },
        17.99: {
            'bought': 806,
            'discount_superior': 990 / 1400,
            'discount': 1090 / 1400,
            'price': 1400,
            'weight': 700,
        },
        19.99: {
            'bought': 942,
            'discount_superior': 1190 / 1600,
            'discount': 1290 / 1600,
            'price': 1600,
            'weight': 700,
        },
        24.99: {
            'bought': 1097,
            'discount_superior': 1290 / 1700,
            'discount': 1390 / 1700,
            'price': 1700,
            'weight': 1000,
        },
        29.99: {
            'bought': 1277,
            'discount_superior': 1590 / 1900,
            'discount': 1690 / 1900,
            'price': 1900,
            'weight': 1500,
        },
        34.99: {
            'bought': 1457,
            'discount_superior': 1690 / 2200,
            'discount': 1890 / 2200,
            'price': 2200,
            'weight': 1900,
        },
        39.99: {
            'bought': 1736,
            'discount_superior': 1990 / 2600,
            'discount': 2190 / 2600,
            'price': 2600,
            'weight': 1900,
        },
        49.99: {
            'bought': 2046,
            'discount_superior': 2490 / 3500,
            'discount': 2690 / 3500,
            'price': 3500,
            'weight': 1900,
        },
        50: {
            'bought': 2046,
            'discount_superior': 2490 / 3500,
            'discount': 2690 / 3500,
            'price': 3500,
            'weight': 1900,
        },
        75: {
            'bought': 2895,
            'discount_superior': 3290 / 5000,
            'discount': 3690 / 5000,
            'price': 5000,
            'weight': 2000,
        },
        99.99: {
            'bought': 4340,
            'discount_superior': 4990 / 7000,
            'discount': 5490 / 7000,
            'price': 7000,
            'weight': 3000,
        },
        100: {
            'bought': 4340,
            'discount_superior': 4990 / 7000,
            'discount': 5490 / 7000,
            'price': 7000,
            'weight': 3000,
        },
        125: {
            'bought': 5611,
            'discount_superior': 6290 / 7000,
            'discount': 6690 / 7000,
            'price': 8000,
            'weight': 3000,
        },
    },
    'weekly': {
        1: {
            'bought': 124,
            'discount': 190 / 300,
            'price': 300,
            'weight': 100,
        },
        2.54: {
            'bought': 219,
            'discount': 350 / 450,
            'price': 450,
            'weight': 100,
        },
        2.99: {
            'bought': 247,
            'discount': 390 / 500,
            'price': 500,
            'weight': 100,
        },
        3.39: {
            'bought': 272,
            'discount': 390 / 500,
            'price': 500,
            'weight': 100,
        },
        3.99: {
            'bought': 309,
            'discount': 450 / 550,
            'price': 550,
            'weight': 100,
        },
        4.24: {
            'bought': 325,
            'discount': 450 / 550,
            'price': 550,
            'weight': 100,
        },
        4.25: {
            'bought': 326,
            'discount': 450 / 550,
            'price': 550,
            'weight': 100,
        },
        5.09: {
            'bought': 378,
            'discount': 490 / 550,
            'price': 550,
            'weight': 100,
        },
        5.94: {
            'bought': 430,
            'discount': 550 / 650,
            'price': 650,
            'weight': 100,
        },
        5.95: {
            'bought': 431,
            'discount': 550 / 650,
            'price': 650,
            'weight': 100,
        },
        6.79: {
            'bought': 483,
            'discount': 630 / 750,
            'price': 750,
            'weight': 100,
        },
        8.49: {
            'bought': 588,
            'discount': 730 / 900,
            'price': 900,
            'weight': 200,
        },
        8.5: {
            'bought': 589,
            'discount': 730 / 900,
            'price': 900,
            'weight': 100,
        },
        10: {
            'bought': 682,
            'discount': 830 / 1000,
            'price': 1000,
            'weight': 100,
        },
        10.2: {
            'bought': 694,
            'discount': 830 / 1000,
            'price': 1000,
            'weight': 100,
        },
        12: {
            'bought': 806,
            'discount': 990 / 1300,
            'price': 1300,
            'weight': 100,
        },
        12.75: {
            'bought': 853,
            'discount': 990 / 1300,
            'price': 1300,
            'weight': 100,
        },
        15.3: {
            'bought': 1011,
            'discount': 1150 / 1400,
            'price': 1400,
            'weight': 100,
        },
        17: {
            'bought': 1116,
            'discount': 1290 / 1500,
            'price': 1500,
            'weight': 100,
        },
        18: {
            'bought': 1178,
            'discount': 1390 / 1600,
            'price': 1600,
            'weight': 100,
        },
        21.25: {
            'bought': 1380,
            'discount': 1590 / 1800,
            'price': 1800,
            'weight': 100,
        },
        25.5: {
            'bought': 1643,
            'discount': 1830 / 2000,
            'price': 2000,
            'weight': 100,
        },
        29.75: {
            'bought': 1907,
            'discount': 2090 / 2500,
            'price': 2500,
            'weight': 100,
        },
        11.04: {
            'bought': 576,
            'discount': 850 / 1100,
            'price': 1100,
            'weight': 700,
        },
        12.74: {
            'bought': 663,
            'discount': 950 / 1250,
            'price': 1250,
            'weight': 700,
        },
        13.59: {
            'bought': 694,
            'discount': 990 / 1300,
            'price': 1300,
            'weight': 700,
        },
        14.44: {
            'bought': 750,
            'discount': 1090 / 1300,
            'price': 1300,
            'weight': 700,
        },
        15.29: {
            'bought': 806,
            'discount': 1190 / 1400,
            'price': 1400,
            'weight': 700,
        },
        16.99: {
            'bought': 942,
            'discount': 1390 / 1600,
            'price': 1600,
            'weight': 700,
        },
        21.24: {
            'bought': 1097,
            'discount': 1490 / 1700,
            'price': 1700,
            'weight': 1000,
        },
        25.49: {
            'bought': 1277,
            'discount': 1790 / 1900,
            'price': 1900,
            'weight': 1500,
        },
        29.74: {
            'bought': 1457,
            'discount': 1990 / 2200,
            'price': 2200,
            'weight': 1900,
        },
        33.99: {
            'bought': 1736,
            'discount': 2390 / 2600,
            'price': 2600,
            'weight': 1900,
        },
        42.49: {
            'bought': 2046,
            'discount': 2890 / 3500,
            'price': 3500,
            'weight': 1900,
        },
        42.5: {
            'bought': 2046,
            'discount': 2890 / 3500,
            'price': 3500,
            'weight': 1900,
        },
        63.75: {
            'bought': 2895,
            'discount': 3890 / 5000,
            'price': 5000,
            'weight': 2000,
        },
        84.99: {
            'bought': 4340,
            'discount': 5690 / 7000,
            'price': 7000,
            'weight': 3000,
        },
        85: {
            'bought': 4340,
            'discount': 5690 / 7000,
            'price': 7000,
            'weight': 3000,
        },
        106.25: {
            'bought': 5611,
            'discount': 6990 / 8000,
            'price': 8000,
            'weight': 3000,
        },
    },
}


PUBLISHERS = [
    {
        'short_name': 'Marvel',
        'full_name': 'Marvel Comics',
        'category': None,
        'abbr': 'MARVEL',
        'midtown_code': '75,110',
        'load_weekly': True,
    },
    {
        'short_name': 'DC',
        'full_name': 'DC Comics',
        'category': None,
        'abbr': 'DC',
        'midtown_code': '71,105',
        'load_weekly': True,
    },
    {
        'short_name': 'Image',
        'full_name': 'Image Comics',
        'category': None,
        'abbr': 'IMAGE',
        'midtown_code': '74,112',
        'load_weekly': True,
    },
    {
        'short_name': 'IDW',
        'full_name': 'IDW Publishing',
        'category': None,
        'abbr': 'IDW',
        'midtown_code': '140,141',
        'load_weekly': True,
    },
    {
        'short_name': 'Dark Horse',
        'full_name': 'Dark Horse Comics',
        'category': None,
        'abbr': 'DH',
        'midtown_code': '77,127',
        'load_weekly': False,
    },
]


class Preview(Item):
    price_origin = models.FloatField(
        default=0.0,
        verbose_name='Оригинальная цена',
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

    session_timestamp = models.FloatField(
        default=0.0,
        verbose_name='Сессия',
    )


class Monthly(Preview):
    discount_superior = models.FloatField(
        default=1.0,
        verbose_name='Множитель скидки superior',
    )


class Weekly(Preview):
    midtown_id = models.CharField(
        default='',
        max_length=64,
        verbose_name='Код Midtown',
    )
