from unicodedata import category
from django.db import models
from goods.models import Categories, Products

from users.models import User


class OrderitemQueryset(models.QuerySet):
    
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    

class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name="Пользователь", default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    
    PRICE_MODEL_CHOICES = [
        ('CPC', 'За количество щелчков мышью(СPC)'),
        ('CPM', 'За количество показов(CPM)'),
        ('CPA', 'За количество действий(CPA)'),
    ]
    price_model = models.CharField(max_length=3, choices=PRICE_MODEL_CHOICES, verbose_name="Выбор ценовой модели")
    
    PAYMENT_ON_GET_CHOICES = [
        ('card', 'Карта'),
        ('ewallet', 'Электронные деньги'),
    ]
    
    payment_on_get = models.CharField(max_length=10, choices=PAYMENT_ON_GET_CHOICES, verbose_name="Способ оплаты")


    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(to=Products, on_delete=models.SET_DEFAULT, null=True, verbose_name="Продукт", default=None)
    name = models.CharField(max_length=150, verbose_name="Название")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")


    class Meta:
        db_table = "order_item"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"

    objects = OrderitemQueryset.as_manager()

    def products_price(self):
        return round(self.product.price, 2)

    def __str__(self):
        return f"Товар {self.name} | Заказ № {self.order.pk}"