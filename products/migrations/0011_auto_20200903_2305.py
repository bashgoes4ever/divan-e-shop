# Generated by Django 3.0.6 on 2020-09-03 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_category_lift_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='casing',
            name='categories',
        ),
        migrations.AddField(
            model_name='casing',
            name='category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='products.CasingCategory', verbose_name='Категория'),
        ),
    ]
