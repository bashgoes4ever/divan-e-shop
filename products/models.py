from django.db import models
from utils.slugify import slugify
from utils.make_thumbnail import make_thumbnail
from django.db.models.signals import post_save, post_delete
from functools import wraps


class Category(models.Model):
    name = models.CharField(max_length=128, blank=False, verbose_name=u"Название")
    parent_category = models.ForeignKey("self", blank=True, null=True, default=None, related_name='children',
                                    on_delete=models.SET_DEFAULT, verbose_name=u"Родительская категория")
    slug = models.SlugField(blank=True)
    is_main = models.BooleanField(default=False, verbose_name=u"Выводить на главной?")
    priority = models.IntegerField(default=1, verbose_name=u"Приоритет")
    level = models.IntegerField(verbose_name=u"Уровень", blank=True, default=0)
    img = models.ImageField(upload_to='static/img/categories/', verbose_name=u"Изображение", blank=True)
    img_thumb = models.ImageField(upload_to='static/img/categories/', blank=True, editable=False)
    delivery_price = models.IntegerField(verbose_name=u"Стоимость доставки", null=True, blank=True)
    lift_price = models.IntegerField(verbose_name=u"Стоимость подъема", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Категория"
        verbose_name_plural = u"Категории"

    def save(self, *args, **kwargs):
        if self.parent_category:
            self.level = self.parent_category.level + 1
        self.slug = slugify(self.name)
        if not make_thumbnail(self.img, self.img_thumb):
            raise Exception('Could not create thumbnail - is the file type valid?')
        super().save(*args, **kwargs)


class Mechanism(models.Model):
    name = models.CharField(max_length=128, blank=False, verbose_name=u"Название")

    class Meta:
        verbose_name = u"Механизм"
        verbose_name_plural = u"Механизмы"

    def __str__(self):
        return self.name


class CategoryMechanism(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True, default=None,
                                    on_delete=models.SET_DEFAULT, verbose_name=u"Категория")
    mechanism = models.ForeignKey(Mechanism, blank=True, null=True, default=None,
                                    on_delete=models.SET_DEFAULT, verbose_name=u"Механизм")


class FrameMaterial(models.Model):
    name = models.CharField(max_length=128, blank=False, verbose_name=u"Название")

    class Meta:
        verbose_name = u"Материал каркаса"
        verbose_name_plural = u"Материалы каркаса"

    def __str__(self):
        return self.name


class UpholsteryMaterial(models.Model):
    name = models.CharField(max_length=128, blank=False, verbose_name=u"Название")

    class Meta:
        verbose_name = u"Материал обивки"
        verbose_name_plural = u"Материалы обивки"

    def __str__(self):
        return self.name


class FillerMaterial(models.Model):
    name = models.CharField(max_length=128, blank=False, verbose_name=u"Название")

    class Meta:
        verbose_name = u"Материал наполнителя"
        verbose_name_plural = u"Материалы наполнителя"

    def __str__(self):
        return self.name


class SupportMaterial(models.Model):
    name = models.CharField(max_length=128, blank=False, verbose_name=u"Название")

    class Meta:
        verbose_name = u"Материал опор"
        verbose_name_plural = u"Материалы опор"

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=128, blank=False, verbose_name=u"Название")

    class Meta:
        verbose_name = u"Страна"
        verbose_name_plural = u"Страны"

    def __str__(self):
        return self.name


class CasingCategory(models.Model):
    name = models.CharField(max_length=128, blank=False, verbose_name=u"Название")
    parent_category = models.ForeignKey("self", blank=True, null=True, default=None, related_name='children',
                                    on_delete=models.SET_DEFAULT, verbose_name=u"Родительская категория")
    slug = models.SlugField(blank=True)
    level = models.IntegerField(verbose_name=u"Уровень", blank=True, default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Категория обивок"
        verbose_name_plural = u"Категории обивок"

    def save(self, *args, **kwargs):
        if self.parent_category:
            self.level = self.parent_category.level + 1
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Casing(models.Model):
    name = models.CharField(max_length=128, blank=False, verbose_name=u"Название")
    img = models.ImageField(upload_to='static/img/products/', verbose_name=u"Изображение", blank=False)
    img_thumb = models.ImageField(upload_to='static/img/products/', blank=True, editable=False)
    category = models.ForeignKey(CasingCategory, blank=True, null=True, default=None,
                                    on_delete=models.SET_DEFAULT, verbose_name=u"Категория")

    class Meta:
        verbose_name = u"Обивка"
        verbose_name_plural = u"Обивки"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not make_thumbnail(self.img, self.img_thumb):
            raise Exception('Could not create thumbnail - is the file type valid?')
        super().save(*args, **kwargs)


class Color(models.Model):
    name = models.CharField(max_length=128, blank=False, verbose_name=u"Название")
    img = models.ImageField(upload_to='static/img/products/', verbose_name=u"Изображение", blank=False)
    img_thumb = models.ImageField(upload_to='static/img/products/', blank=True, editable=False)

    class Meta:
        verbose_name = u"Цвет ножек"
        verbose_name_plural = u"Цвета ножек"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not make_thumbnail(self.img, self.img_thumb):
            raise Exception('Could not create thumbnail - is the file type valid?')
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=128, blank=False, verbose_name=u"Полное название")
    slug = models.SlugField(blank=True)
    catalog_name = models.CharField(max_length=128, blank=False, verbose_name=u"Сокращенное название")
    category = models.ForeignKey(Category, blank=True, null=True, default=None,
                                    on_delete=models.SET_DEFAULT, verbose_name=u"Категория")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=u"Текущая цена")
    old_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=u"Старая цена", blank=True, null=True)
    in_stock = models.BooleanField(default=True, verbose_name=u"В наличии?")
    casings = models.ManyToManyField(Casing, blank=True, default=None, verbose_name=u"Обивки")
    colors = models.ManyToManyField(Color, blank=True, default=None, verbose_name=u"Цвета ножек")
    description = models.TextField(max_length=512, blank=True, verbose_name=u"Описание")
    priority = models.IntegerField(default=1, verbose_name=u"Приоритет")
    similar_products = models.ManyToManyField("self", blank=True, default=None, verbose_name=u"Похожие товары")
    mechanism = models.ForeignKey(Mechanism, blank=True, null=True, default=None,
                                    on_delete=models.SET_DEFAULT, verbose_name=u"Механизм трансформации")
    frame_material = models.ManyToManyField(FrameMaterial, blank=True, default=None, verbose_name=u"Материал каркаса")
    upholstery_material = models.ManyToManyField(UpholsteryMaterial, blank=True, default=None, verbose_name=u"Материал обивки")
    filler_material = models.ManyToManyField(FillerMaterial, blank=True, default=None, verbose_name=u"Материал наполнителя")
    support_material = models.ManyToManyField(SupportMaterial, blank=True, default=None, verbose_name=u"Материал опор")
    width = models.IntegerField(null=True, blank=True, verbose_name=u"Ширина, см")
    depth = models.IntegerField(null=True, blank=True, verbose_name=u"Глубина, см")
    height = models.IntegerField(null=True, blank=True, verbose_name=u"Высота, см")
    bed_width = models.IntegerField(null=True, blank=True, verbose_name=u"Ширина спального места, см")
    bed_length = models.IntegerField(null=True, blank=True, verbose_name=u"Длина спального места, см")
    weight = models.IntegerField(null=True, blank=True, verbose_name=u"Вес, кг")
    volume = models.IntegerField(null=True, blank=True, verbose_name=u"Объем, куб. м")
    size = models.IntegerField(null=True, blank=True, verbose_name=u"Размер в разложенном виде, см")
    box = models.IntegerField(null=True, blank=True, verbose_name=u"Бельевой ящик, см")
    has_pillows = models.BooleanField(default=False, verbose_name=u"Наличие декоративных подушек")
    has_armrests = models.BooleanField(default=False, verbose_name=u"Наличие подлокотников")
    linings = models.CharField(max_length=128, blank=True, verbose_name=u"Деревяные накладки")
    has_guaranty = models.BooleanField(default=True, verbose_name=u"Гарантия")
    country = models.ForeignKey(Country, blank=True, null=True, default=None,
                                    on_delete=models.SET_DEFAULT, verbose_name=u"Страна")
    features_description = models.TextField(max_length=512, blank=True, verbose_name=u"Описание особенностей")
    added_to_basket = models.IntegerField(default=0, blank=True, null=True, verbose_name=u"Товар добавлен в корзину, раз")
    purchased = models.IntegerField(default=0, blank=True, null=True, verbose_name=u"Товар куплен, раз")

    class Meta:
        verbose_name = u"Товар"
        verbose_name_plural = u"Товары"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True, default=None, related_name='images',
                                    on_delete=models.SET_DEFAULT, verbose_name=u"Товар")
    img = models.ImageField(upload_to='static/img/products/', verbose_name=u"Изображение", blank=False)
    img_thumb = models.ImageField(upload_to='static/img/products/', blank=True, editable=False)
    priority = models.IntegerField(default=1, verbose_name=u"Приоритет")

    class Meta:
        verbose_name = u"Изображение"
        verbose_name_plural = u"Изображения"

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not make_thumbnail(self.img, self.img_thumb):
            raise Exception('Could not create thumbnail - is the file type valid?')
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


def get_all_categories(category, res=None):
    if res is None:
        res = []
    res.append(category.id)
    if category.level >= 1:
        return get_all_categories(category.parent_category, res)
    else:
        return res


def create_category_mechanism(cat_id, mechanism):
    category_mechanisms = CategoryMechanism.objects.filter(category_id=cat_id)
    for item in category_mechanisms:
        if item.mechanism == mechanism:
            return True
    CategoryMechanism.objects.create(category_id=cat_id, mechanism=mechanism).save()


@disable_for_loaddata
def product_post_save(sender, instance, created, **kwargs):
    category = instance.category
    categories = get_all_categories(category)
    mechanism = instance.mechanism
    if mechanism:
        for category_id in categories:
            create_category_mechanism(category_id, mechanism)


# def product_post_delete(sender, instance, **kwargs):
#     order = instance.order
#     all_products = Order.objects.get(id=order.id).productinbasket_set.all()
#     order_total_price = 0
#     for item in all_products:
#         order_total_price += item.total_price
#     instance.order.total_price = order_total_price
#     instance.order.save(force_update=True)


post_save.connect(product_post_save, sender=Product)
# post_delete.connect(product_post_delete, sender=Product)