from django.db import models
from django.utils.timezone import now
from products.models import Product, Color, Casing
from django.db.models.signals import post_save, post_delete
from functools import wraps


class Basket(models.Model):
    user = models.CharField(max_length=128, blank=False, verbose_name=u"Пользователь")  # session key
    start_date = models.DateTimeField(default=now, editable=False, verbose_name=u"Создание корзины")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=u"Общая стоимость")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


def get_delivery_price(category):
    if category.delivery_price:
        return category.delivery_price
    else:
        return get_delivery_price(category.parent_category)
    return 0


class ProductInBasket(models.Model):
    basket = models.ForeignKey(Basket, blank=True, null=True, default=None, related_name="products",
                                    on_delete=models.CASCADE, verbose_name=u"Корзина")
    product = models.ForeignKey(Product, blank=True, null=True, default=None,
                                    on_delete=models.CASCADE, verbose_name=u"Товар")
    quantity = models.IntegerField(verbose_name=u"Количество", blank=True, default=1)
    color = models.ForeignKey(Color, blank=True, null=True, default=None,
                                    on_delete=models.CASCADE, verbose_name=u"Цвет ножек")
    casing = models.ForeignKey(Casing, blank=True, null=True, default=None,
                                    on_delete=models.CASCADE, verbose_name=u"Обивка")
    delivery_price = models.IntegerField(verbose_name=u"Стоимость доставки", null=True, blank=True)

    def __str__(self):
        return str(self.product.catalog_name)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        self.delivery_price = get_delivery_price(self.product.category)
        super().save(*args, **kwargs)


def disable_for_loaddata(signal_handler):
    """
    Decorator that turns off signal handlers when loading fixture data.
    """
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs['raw']:
            return
        signal_handler(*args, **kwargs)
    return wrapper


@disable_for_loaddata
def product_post_save(sender, instance, created, **kwargs):
    basket = instance.basket
    total_price = 0
    for product in basket.products.all():
        total_price = total_price + product.product.price * product.quantity
    basket.total_price = total_price
    basket.save(force_update=True)


def product_post_delete(sender, instance, **kwargs):
    basket = instance.basket
    price = instance.product.price * instance.quantity
    basket.total_price = basket.total_price - price
    product = instance.product
    product.added_to_basket = product.added_to_basket - 1
    product.save(force_update=True)
    basket.save(force_update=True)


post_save.connect(product_post_save, sender=ProductInBasket)
post_delete.connect(product_post_delete, sender=ProductInBasket)

