from django.db import models, IntegrityError
from accounts.models import User
from jsonfield import JSONField


DEFAULT_WEIGHT = 100


class Category(models.Model):
    title = models.CharField(
        default='',
        max_length=16,
        verbose_name='Название',
    )

    parent = models.ForeignKey(
        'self',
        null=True,
        on_delete=models.CASCADE,
    )

    def is_root(self):
        if self.parent is None:
            return True
        else:
            return False

    def set_parent(self, other):
        if self != other:
            self.parent = other
            self.save()
        else:
            raise IntegrityError('Category can\'t refer to itself')


class Item(models.Model):
    title = models.CharField(
        default='Без названия',
        max_length=512,
        verbose_name='Название',
    )

    description = models.TextField(
        default='',
        verbose_name='Описание',
    )

    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
    )

    publisher = models.CharField(
        default='',
        max_length=32,
        verbose_name='Издатель',
    )

    bought = models.FloatField(
        default=0,
        verbose_name='Закупочная цена'
    )

    price = models.FloatField(
        default=0,
        verbose_name='Цена',
    )

    discount = models.FloatField(
        default=1.0,
        verbose_name='Множитель скидки',
    )

    quantity = models.IntegerField(
        null=True,
        default=0,
        verbose_name='Количество',
    )

    weight = models.FloatField(
        default=DEFAULT_WEIGHT,
        verbose_name='Вес',
    )

    cover_list = JSONField(
        default='',
        verbose_name='Список обложек',
    )

    active = models.BooleanField(
        default=False,
        verbose_name='Активен',
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан',
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлен',
    )


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    content = JSONField(
        default='',
        verbose_name='Содержимое',
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлен',
    )

    def clear(self):
        self.content = []


class PaymentMethod(models.Model):
    name = models.CharField(
        default='',
        max_length=32,
        verbose_name='Название',
    )

    description = models.TextField(
        default='',
        verbose_name='Описание',
    )


class DeliveryMethod(models.Model):
    name = models.CharField(
        default='',
        max_length=32,
        verbose_name='Название',
    )

    description = models.TextField(
        default='',
        verbose_name='Описание',
    )


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    content = JSONField(
        default='',
        verbose_name='Содержимое',
    )

    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.CASCADE,
        verbose_name='Метод оплаты',
    )

    delivery_method = models.ForeignKey(
        DeliveryMethod,
        on_delete=models.CASCADE,
        verbose_name='Метод доставки',
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан',
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлен',
    )
