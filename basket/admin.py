from django.contrib import admin
from .models import *


class ProductInBasketInline(admin.TabularInline):
    model = ProductInBasket
    extra = 1


class BasketAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Basket._meta.fields]
    inlines = [ProductInBasketInline]
    ordering = ('start_date',)

    class Meta:
        model = Basket


admin.site.register(Basket, BasketAdmin)
admin.site.register(ProductInBasket)
