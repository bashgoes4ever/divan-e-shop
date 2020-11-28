from django.db import models
from classess import SingletonModel


class Slide(models.Model):
    title_main = models.TextField(max_length=256, blank=True, verbose_name=u"Главный заголовок")
    title_second = models.TextField(max_length=256, blank=True, verbose_name=u"Второй заголовок")
    text = models.TextField(max_length=256, blank=True, verbose_name=u"Подзаголовок")
    link = models.CharField(max_length=256, blank=True, verbose_name=u"Ссылка")
    link_text = models.CharField(max_length=256, blank=True, verbose_name=u"Текст кнопки")
    img = models.ImageField(upload_to='static/img/slides/', verbose_name=u"Изображение", blank=True)
    priority = models.IntegerField(default=1, verbose_name=u"Приоритет")

    class Meta:
        verbose_name = u"Слайд на главной странице"
        verbose_name_plural = u"Слайды на главной странице"

    def __str__(self):
        return self.title_main


class Contacts(SingletonModel.SingletonModel):
    phone1 = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"Телефон для оформления заказа")
    email1 = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"Email для оформления заказа")
    phone2 = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"Телефон для сотрудничества")
    email2 = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"Email для сотрудничества")
    work_time = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"Время работы")
    shop_address = models.TextField(max_length=512, blank=True, null=True, verbose_name=u"Адрес магазина")
    shop_map = models.TextField(max_length=512, blank=True, null=True, verbose_name=u"Код карты")
    instagram = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"Instagram")
    facebook = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"Facebook")

    def __str__(self):
        return u"Контакты"

    class Meta:
        verbose_name = u"Контакты"
        verbose_name_plural = u"Контакты"
