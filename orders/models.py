from django.db import models
from django.utils.timezone import now
from products.models import Product, Color, Casing
from django.db.models.signals import post_save, post_delete
from functools import wraps
from django.core.mail import send_mail


class Order(models.Model):
    customer_name = models.CharField(max_length=128, blank=True, verbose_name=u"Ф.И.О.")
    customer_phone = models.CharField(max_length=128, blank=False, verbose_name=u"Телефон")
    customer_email = models.CharField(max_length=128, blank=False, verbose_name=u"Email")
    customer_city = models.CharField(max_length=128, blank=True, verbose_name=u"Город")
    customer_address = models.CharField(max_length=128, blank=True, verbose_name=u"Адрес")
    comment = models.TextField(max_length=512, blank=True, null=True, verbose_name=u"Комментарий")
    payment_type = models.CharField(max_length=128, blank=False, verbose_name=u"Способ оплаты")
    start_date = models.DateTimeField(default=now, editable=False, verbose_name=u"Создание заказа")
    status = models.CharField(max_length=128, blank=False, default='Не оплачен', verbose_name=u"Статус")
    delivery = models.BooleanField(default=True, verbose_name=u"Доставка")
    products_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=u"Стоимость товаров")
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, verbose_name=u"Стоимость доставки")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=u"Общая стоимость")

    def __str__(self):
        return str(self.customer_email) + ' ' + str(self.start_date)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):
        if not self.pk:
            message = '''
                Создан новый заказ. Зайдите в админ панель, чтобы посмотреть подробности.
                Общая стоимость: {}
                Дата создания: {}
                '''.format(self.total_price, self.start_date)
            send_mail(
                u'Заявка с сайта',
                message,
                'mail@axis-marketing.ru',
                ['marukhelin@gmail.com'],
                fail_silently=True,
            )
        super().save(*args, **kwargs)


def get_delivery_price(category):
    if category.delivery_price:
        return category.delivery_price
    else:
        return get_delivery_price(category.parent_category)
    return 0


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None, related_name="products",
                                    on_delete=models.CASCADE, verbose_name=u"Заказ")
    product = models.ForeignKey(Product, blank=True, null=True, default=None,
                                    on_delete=models.CASCADE, verbose_name=u"Товар")
    quantity = models.IntegerField(verbose_name=u"Количество", blank=True, default=1)
    color = models.ForeignKey(Color, blank=True, null=True, default=None,
                                    on_delete=models.CASCADE, verbose_name=u"Цвет ножек")
    casing = models.ForeignKey(Casing, blank=True, null=True, default=None,
                                    on_delete=models.CASCADE, verbose_name=u"Обивка")
    price = models.IntegerField(verbose_name=u"Стоимость товара на момент заказа", null=True, blank=True)
    delivery_price = models.IntegerField(verbose_name=u"Стоимость доставки", null=True, blank=True)

    def __str__(self):
        return str(self.product.catalog_name)

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def save(self, *args, **kwargs):
        self.delivery_price = get_delivery_price(self.product.category)
        self.price = self.product.price
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
    order = instance.order
    products_price = 0
    delivery_price = 0
    for product in order.products.all():
        products_price = products_price + product.product.price * product.quantity
        delivery_price = delivery_price + product.delivery_price * product.quantity
    order.products_price = products_price
    order.delivery_price = delivery_price
    if order.delivery:
        order.total_price = products_price + delivery_price
    else:
        order.total_price = products_price
    product = instance.product
    product.purchased = product.purchased + 1
    product.save(force_update=True)
    order.save(force_update=True)


def product_post_delete(sender, instance, **kwargs):
    order = instance.order
    price = instance.product.price * instance.quantity
    order.products_price = order.products_price - price
    order.delivery_price = order.delivery_price - instance.delivery_price * instance.quantity
    order.total_price = order.total_price - (price + (instance.delivery_price * instance.quantity))
    product = instance.product
    product.purchased = product.purchased - 1
    product.save(force_update=True)
    order.save(force_update=True)


post_save.connect(product_post_save, sender=ProductInOrder)
post_delete.connect(product_post_delete, sender=ProductInOrder)
