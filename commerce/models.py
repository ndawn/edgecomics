from django.db import models, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from django_mysql.models import JSONField
from accounts.models import User


DEFAULT_WEIGHT = 100


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(
        default='',
        max_length=32,
        verbose_name='Название',
    )

    description = models.TextField(
        default='',
        blank=True,
        verbose_name='Описание',
    )

    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Родительская категория',
    )

    def as_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'parent': self.parent.as_dict() if self.parent is not None else None,
        }

    def is_root(self):
        if self.parent is None:
            return True
        else:
            return False

    def set_parent(self, other):
        if not isinstance(other, Category):
            raise IntegrityError('Parent must be a category')
        if self == other:
            raise IntegrityError('Category can\'t refer to itself')
        else:
            self.parent = other
            self.save()

    def get_root(self):
        if self.is_root():
            return self
        else:
            return self.parent.get_root()

    @staticmethod
    def get_list():
        return [cat.as_dict() for cat in Category.objects.all()]

    def get_parent_chain(self):
        return [self.title] + (self.parent.get_parent_chain() if self.parent is not None else [])

    def __str__(self):
        return ' -> '.join(reversed(self.get_parent_chain()))


class Item(models.Model):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    title = models.CharField(
        default='Без названия',
        blank=True,
        max_length=512,
        verbose_name='Название',
    )

    description = models.TextField(
        default='',
        blank=True,
        verbose_name='Описание',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория',
    )

    publisher = models.CharField(
        default='',
        blank=True,
        max_length=32,
        verbose_name='Издатель',
    )

    bought = models.FloatField(
        default=0,
        blank=True,
        verbose_name='Закупочная цена'
    )

    price = models.FloatField(
        default=0,
        blank=True,
        verbose_name='Цена',
    )

    discount = models.FloatField(
        default=1.0,
        blank=True,
        verbose_name='Множитель скидки',
    )

    quantity = models.IntegerField(
        null=True,
        default=0,
        blank=True,
        verbose_name='Количество',
    )

    weight = models.FloatField(
        default=DEFAULT_WEIGHT,
        blank=True,
        verbose_name='Вес',
    )

    cover_list = JSONField(
        default=dict,
        blank=True,
        verbose_name='Список обложек',
    )

    active = models.BooleanField(
        default=False,
        blank=True,
        verbose_name='Активен',
    )

    created = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        verbose_name='Создан',
    )

    updated = models.DateTimeField(
        auto_now=True,
        blank=True,
        verbose_name='Обновлен',
    )

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.title,
            'category': self.category.as_dict() if self.category is not None else None,
            'publisher': self.publisher,
            'price': self.price,
            'discount': self.discount,
            'quantity': self.quantity,
            'weight': self.weight,
            'cover_list': self.cover_list,
        }

    def __str__(self):
        return ((self.category.get_root().title + ' -> ') if self.category is not None else '') + self.title


class CartItem(models.Model):
    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'

        unique_together = ('user', 'item')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name='Пользователь',
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Товар',
    )

    quantity = models.IntegerField(
        default=1,
        blank=True,
        verbose_name='Количество',
    )

    created = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        verbose_name='Создан',
    )

    updated = models.DateTimeField(
        auto_now=True,
        blank=True,
        verbose_name='Обновлен',
    )

    def in_stock(self):
        return (self.item.quantity != 0) or (self.item.quantity is None)

    def as_dict(self):
        return {
            'id': self.id,
            'quantity': self.quantity,
            'item': self.item.as_dict(),
        }

    class _Cart:
        @staticmethod
        def get(obj):
            if isinstance(obj, User):
                return CartItem.objects.filter(user=obj)
            elif isinstance(obj, int):
                return CartItem.objects.filter(user__id=obj)
            else:
                return CartItem.objects.none()

        @staticmethod
        def get_list(obj):
            if isinstance(obj, User):
                return [item.as_dict() for item in CartItem.objects.filter(user=obj)]
            elif isinstance(obj, int):
                return [item.as_dict() for item in CartItem.objects.filter(user__id=obj)]
            elif isinstance(obj, QuerySet) or isinstance(obj, list):
                return [item.as_dict() for item in obj]
            else:
                return []

        @staticmethod
        def add(user, obj):
            try:
                if isinstance(obj, Item):
                    if isinstance(user, User):
                        return CartItem.objects.create(user=user, item=obj).as_dict()
                    elif isinstance(user, int):
                        return CartItem.objects.create(user__id=user, item=obj).as_dict()
                elif isinstance(obj, int):
                    try:
                        item = Item.objects.get(id=obj)
                    except ObjectDoesNotExist:
                        return

                    if not item.active:
                        return
                    elif isinstance(user, User):
                        return CartItem.objects.create(user=user, item=item).as_dict()
                    elif isinstance(user, int):
                        return CartItem.objects.create(user__id=user, item=item).as_dict()
                    else:
                        return
            except IntegrityError:
                return

        @staticmethod
        def remove(obj):
            if isinstance(obj, CartItem):
                return obj.delete()
            elif isinstance(obj, int):
                try:
                    return CartItem.objects.get(id=obj).delete()
                except ObjectDoesNotExist:
                    return CartItem.objects.none().delete()
            else:
                return CartItem.objects.none().delete()

        @staticmethod
        def update(obj, quantity):
            if not isinstance(quantity, int):
                return False, 'invalid request'

            if isinstance(obj, CartItem):
                item = obj
            elif isinstance(obj, int):
                try:
                    item = CartItem.objects.get(id=obj)
                except ObjectDoesNotExist:
                    return False, 'object does not exist', 404
            else:
                return False, 'invalid request', 400

            if item.item.quantity is not None:
                if (quantity > 0) and (quantity <= item.item.quantity):
                    item.quantity = quantity
                    item.save()

                    return True, {
                        'id': item.id,
                        'quantity': item.quantity,
                    }
                elif quantity <= 0:
                    CartItem.cart.remove(item)

                    return True, {
                        'id': None,
                        'quantity': 0,
                    }
                else:
                    item.quantity = item.item.quantity
                    item.save()

                    return True, {
                        'id': item.id,
                        'quantity': item.quantity,
                    }
            else:
                item.quantity = quantity
                item.save()

                return True, {
                    'id': item.id,
                    'quantity': item.quantity,
                }

        @staticmethod
        def clear(obj):
            if isinstance(obj, User):
                return CartItem.objects.filter(user=obj).delete()
            elif isinstance(obj, int):
                return CartItem.objects.filter(user__id=obj).delete()
            elif isinstance(obj, QuerySet):
                return obj.delete()
            else:
                return CartItem.objects.none().delete()

    cart = _Cart


class PaymentMethod(models.Model):
    class Meta:
        verbose_name = 'Метод оплаты'
        verbose_name_plural = 'Методы оплаты'

    name = models.CharField(
        default='',
        blank=True,
        max_length=32,
        verbose_name='Название',
    )

    description = models.TextField(
        default='',
        blank=True,
        verbose_name='Описание',
    )


class DeliveryMethod(models.Model):
    class Meta:
        verbose_name = 'Метод доставки'
        verbose_name_plural = 'Методы доставки'

    name = models.CharField(
        default='',
        blank=True,
        max_length=32,
        verbose_name='Название',
    )

    description = models.TextField(
        default='',
        blank=True,
        verbose_name='Описание',
    )


class OrderStatus(models.Model):
    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'

    name = models.CharField(
        default='',
        blank=True,
        max_length=64,
        verbose_name='Название',
    )

    description = models.CharField(
        default='',
        blank=True,
        max_length=128,
        verbose_name='Описание',
    )


class Order(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Пользователь',
    )

    content = JSONField(
        default=list,
        blank=True,
        verbose_name='Содержимое',
    )

    payment_method = models.ForeignKey(
        PaymentMethod,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Метод оплаты',
    )

    delivery_method = models.ForeignKey(
        DeliveryMethod,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Метод доставки',
    )

    track_code = models.CharField(
        blank=True,
        null=True,
        max_length=32,
        verbose_name='Код отслеживания',
    )

    status = models.ForeignKey(
        OrderStatus,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Статус',
    )

    created = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        verbose_name='Создан',
    )

    updated = models.DateTimeField(
        auto_now=True,
        blank=True,
        verbose_name='Обновлен',
    )
