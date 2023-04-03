from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count
from django.template.defaultfilters import slugify
from django.urls import reverse


class Category(models.Model):
    """Категории"""
    name = models.CharField("категория", max_length=150)

    url = models.SlugField(max_length=160)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Gender(models.Model):
    """Пол"""
    name = models.CharField("пол", max_length=50)

    url = models.SlugField(max_length=160)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "пол"
        verbose_name_plural = "пол"


class Product(models.Model):
    """Товары"""
    gender = models.ForeignKey(
        Gender, verbose_name="пол", on_delete=models.SET_NULL, null=True
    )
    category = models.ForeignKey(
        Category, verbose_name="категория", on_delete=models.SET_NULL, null=True
    )
    photo = models.ImageField("фото", upload_to="products/", null=True)
    type = models.CharField("тип", max_length=100)
    color = models.CharField("цвет", max_length=100)
    price = models.DecimalField("цена", max_digits=20, decimal_places=0)
    description = models.TextField("описание", blank=True) # blank=True - Пустая строка=Имеет право существовать

    url = models.SlugField(max_length=160)

    def __str__(self):
        return f"{self.gender} - {self.category} - {self.type} - {self.color}"


    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.url})

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"


class Sizes(models.Model):
    "Размеры"
    product = models.ForeignKey(
        Product, verbose_name="товар", related_name='sizes', on_delete=models.CASCADE, null=True
    )

    SIZE = [
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    ]
    size = models.CharField("размер товара", max_length=50, choices=SIZE)
    amount_size = models.DecimalField("количество товара данного размера", max_digits=20, decimal_places=0)

    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return f"{self.size} - {self.product}"

    class Meta:
        verbose_name = "размер"
        verbose_name_plural = "размеры"


class Cart(models.Model):
    "Корзина"

    cart_number = models.DecimalField(max_digits=20, decimal_places=0, null=True)

    product = models.ForeignKey(
        Product, verbose_name="товар", related_name='cart', on_delete=models.SET_NULL, blank=False, null=True
    )

    size = models.CharField("размер для корзины", max_length=50)
    amount = models.DecimalField(max_digits=20, decimal_places=0, default=1)
    price = models.DecimalField(max_digits=20, decimal_places=0, default=1)


    def __str__(self):
        return f"{self.product} - {self.size}"

    class Meta:
        verbose_name = "корзина"
        verbose_name_plural = "корзины пользователей"


class Order(models.Model):
    "Заказ"

    order_number = models.DecimalField(max_digits=20, decimal_places=0, null=True)

    product = models.ForeignKey(
        Product, verbose_name="товар", related_name='order', on_delete=models.SET_NULL, blank=False, null=True
    )

    size = models.CharField("размер для заказа", max_length=50)
    amount = models.DecimalField(max_digits=20, decimal_places=0, default=1)
    price = models.DecimalField(max_digits=20, decimal_places=0, default=1)
    status_payment = models.CharField(max_length=50, default='Не оплачено')
    url = models.SlugField(max_length=160)


    def __str__(self):
        return f"{self.product} - {self.size} - {self.amount} - {self.price}"

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "Заказы пользователей"


class PaymentOrder(models.Model):

    payment_order_number = models.CharField("номер заказа для оплаты", max_length=50)
    delivery_address = models.CharField("адрес доставки", max_length=50)
    delivery_period = models.CharField("время доставки", max_length=50)
    phone_user = models.CharField("время доставки", max_length=50)
    payment_status = models.CharField("статус оплаты", max_length=50)
    delivery_status = models.CharField("статус доставки", max_length=50)

    def __str__(self):
        return f"{self.delivery_address} - {self.delivery_period} - {self.phone_user} - {self.payment_status} - {self.delivery_status}"

    class Meta:
        verbose_name = "заказ для оплаты"
        verbose_name_plural = "Заказы с оплатой"
