# Generated by Django 3.0.6 on 2020-09-03 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0002_auto_20200903_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='productinbasket',
            name='delivery_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Стоимость доставки'),
        ),
    ]
