from rest_framework import serializers
from .models import *


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        fields = {
            'customer_name': validated_data.get('customer_name'),
            'customer_phone': validated_data.get('customer_phone'),
            'customer_email': validated_data.get('customer_email'),
            'customer_city': validated_data.get('customer_city'),
            'customer_address': validated_data.get('customer_address'),
            'comment': validated_data.get('comment'),
            'payment_type': validated_data.get('payment_type'),
            'delivery': validated_data.get('delivery'),
        }
        order, created = Order.objects.get_or_create(**fields)
        return order