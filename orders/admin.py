from django.contrib import admin
from .models import *


class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    inlines = [ProductInOrderInline]
    ordering = ('-start_date',)
    fieldsets = (
        ('Информация о покупателе', {'fields': (
            'customer_name', 'customer_phone', 'customer_email', 'customer_city', 'customer_address', 'comment')}),
        ('Информация об оплате',
         {'fields': ('payment_type', 'status', 'products_price', 'delivery', 'delivery_price', 'total_price')}),
    )

    class Meta:
        model = Order


admin.site.register(Order, OrderAdmin)
admin.site.register(ProductInOrder)
