# Generated by Django 3.0.6 on 2020-09-03 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone1', models.CharField(blank=True, max_length=128, null=True, verbose_name='Телефон для оформления заказа')),
                ('email1', models.CharField(blank=True, max_length=128, null=True, verbose_name='Email для оформления заказа')),
                ('phone2', models.CharField(blank=True, max_length=128, null=True, verbose_name='Телефон для сотрудничества')),
                ('email2', models.CharField(blank=True, max_length=128, null=True, verbose_name='Email для сотрудничества')),
                ('work_time', models.CharField(blank=True, max_length=128, null=True, verbose_name='Время работы')),
                ('shop_address', models.TextField(blank=True, max_length=512, null=True, verbose_name='Адрес магазина')),
                ('shop_map', models.TextField(blank=True, max_length=512, null=True, verbose_name='Код карты')),
                ('instagram', models.CharField(blank=True, max_length=128, null=True, verbose_name='Instagram')),
                ('facebook', models.CharField(blank=True, max_length=128, null=True, verbose_name='Facebook')),
            ],
            options={
                'verbose_name': 'Контакты',
                'verbose_name_plural': 'Контакты',
            },
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_main', models.TextField(blank=True, max_length=256, verbose_name='Главный заголовок')),
                ('title_second', models.TextField(blank=True, max_length=256, verbose_name='Второй заголовок')),
                ('text', models.TextField(blank=True, max_length=256, verbose_name='Подзаголовок')),
                ('link', models.CharField(blank=True, max_length=256, verbose_name='Ссылка')),
                ('img', models.ImageField(blank=True, upload_to='static/img/slides/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Слайд на главной странице',
                'verbose_name_plural': 'Слайды на главной странице',
            },
        ),
    ]
