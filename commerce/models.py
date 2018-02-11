from django.db import models, IntegrityError
from django.contrib.postgres.fields import JSONField
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

    slug = models.SlugField(
        blank=True,
        null=True,
        verbose_name='Обозначение',
    )

    background = models.URLField(
        default=None,
        blank=True,
        null=True,
        verbose_name='Фоновое изображение',
    )

    def as_dict(self):
        return {
            'id': self.id,
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

    def self_tree(self):
        tree_list = []

        for category in self.children():
            tree_list.append({
                'category': category,
                'children': category.self_tree(),
            })

        return tree_list

    @staticmethod
    def tree():
        tree_list = []

        for category in Category.objects.filter(parent=None):
            tree_list.append({
                'category': category,
                'children': category.self_tree(),
            })

        return tree_list

    def children(self):
        return list(Category.objects.filter(parent=self))

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
            'description': self.description,
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


class CartManager(models.Manager):
    def get_cart(self, user):
        return self.get_or_create(user=user, is_submitted=False, defaults={'user': user})[0]

    def create_from_anonymous(self, anonymous, user):
        for cart_item in anonymous:
            item_id = cart_item['item']['id']
            item_queryset = Item.objects.in_bulk([item_id])
            item = item_queryset.get(item_id)

            if item and item.quantity:
                if item.quantity >= cart_item['quantity']:
                    quantity = cart_item['quantity']
                else:
                    quantity = item.quantity

                CartItem.objects.create(
                    item=item,
                    quantity=quantity,
                    cart=self.get_cart(user),
                )
        return self.get_cart(user)


class Cart(models.Model):
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    objects = CartManager()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    is_submitted = models.BooleanField(
        default=False,
        verbose_name='Закрыта',
    )

    closed = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
        verbose_name='Закрыта',
    )

    created = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        verbose_name='Создана',
    )

    updated = models.DateTimeField(
        auto_now=True,
        blank=True,
        verbose_name='Обновлена',
    )

    def get_items(self):
        return CartItem.objects.filter(cart=self)

    def clear(self):
        self.get_items().delete()

    def as_dict(self):
        cart = []

        for cart_item in self.get_items():
            cart.append(cart_item.as_dict())

        return cart


class CartItem(models.Model):
    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'

        unique_together = ('cart', 'item')

    item = models.ForeignKey(
        Item,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Товар',
    )

    quantity = models.IntegerField(
        default=1,
        null=True,
        blank=True,
        verbose_name='Количество',
    )

    cart = models.ForeignKey(
        Cart,
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Корзина',
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
            'item': self.item.as_dict(),
            'quantity': self.quantity,
        }


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

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }


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

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }


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

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }


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

    cart = models.ForeignKey(
        Cart,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        verbose_name='Корзина',
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

    def as_dict(self):
        return {
            'id': self.id,
            'user': self.user.as_dict(),
            'content': self.content,
            'payment_method': self.payment_method.as_dict(),
            'delivery_method': self.delivery_method.as_dict(),
            'track_code': self.track_code,
            'status': self.status.as_dict(),
            'created': self.created,
            'updated': self.updated,
        }
