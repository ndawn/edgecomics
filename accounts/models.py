from django.db import models
from django.contrib.auth.models import User as BaseUser


class Address(models.Model):
    country = models.CharField(
        default='',
        max_length=32,
        verbose_name='Страна',
    )

    region = models.CharField(
        default='',
        max_length=128,
        verbose_name='Регион',
    )

    locality = models.CharField(
        default='',
        max_length=64,
        verbose_name='Населенный пункт',
    )

    street = models.CharField(
        default='',
        max_length=256,
        verbose_name='Улица',
    )

    building = models.CharField(
        default='',
        max_length=32,
        verbose_name='Дом, строение, корпус',
    )

    apartment = models.CharField(
        null=True,
        max_length=8,
        verbose_name='Квартира, комната',
    )

    zipcode = models.CharField(
        default='',
        max_length=8,
        verbose_name='Почтовый индекс',
    )


class User(BaseUser):
    def __init__(self):
        super().__init__()

    status = models.SmallIntegerField(
        default=0,
        verbose_name='Статус',
    )

    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        verbose_name='Адрес',
    )
