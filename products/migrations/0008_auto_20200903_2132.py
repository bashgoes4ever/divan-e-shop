# Generated by Django 3.0.6 on 2020-09-03 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_category_delivery_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='delivery_price',
            field=models.IntegerField(null=True, verbose_name='Стоимость доставки'),
        ),
    ]