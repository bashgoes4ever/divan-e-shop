from rest_framework import serializers
from .models import *
from products.serializers import CasingSerializer, ColorSerializer, ProductSerializer


class ProductInBasketViewSerializer(serializers.ModelSerializer):
    casing = CasingSerializer()
    color = ColorSerializer()
    product = ProductSerializer()

    class Meta:
        model = ProductInBasket
        fields = '__all__'


class BasketSerializer(serializers.ModelSerializer):
    products = ProductInBasketViewSerializer(many=True)

    class Meta:
        model = Basket
        exclude = ['id', 'user', 'start_date']


class ProductInBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInBasket
        fields = '__all__'

    def create(self, validated_data):
        session_key = self.context['request'].META['HTTP_AUTHORIZATION']
        basket, created = Basket.objects.get_or_create(user=session_key)
        product = validated_data.get('product')
        color = validated_data.get('color')
        casing = validated_data.get('casing')
        product.added_to_basket = product.added_to_basket + 1
        product.save()
        product_in_basket, created = ProductInBasket.objects.get_or_create(basket=basket, product=product, color=color,
                                                                           casing=casing, quantity=validated_data.get('quantity'))
        return product_in_basket

    def update(self, instance, validated_data):
        session_key = self.context['request'].META['HTTP_AUTHORIZATION']
        basket = instance.basket
        if session_key != basket.user:
            raise serializers.ValidationError('You have no rights to edit this basket.')
        else:
            instance.quantity = int(validated_data.get("quantity", instance.quantity))
            instance.save()
