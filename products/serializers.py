from rest_framework import serializers
from .models import *


class MechanismSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mechanism
        fields = '__all__'


class CategoryMechanismSerializer(serializers.ModelSerializer):
    mechanism = MechanismSerializer()
    class Meta:
        model = CategoryMechanism
        exclude = ['id', 'category']


class CategoryRecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ProductCategoryRecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    children = CategoryRecursiveField(many=True)
    mechanisms = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['name', 'slug', 'children', 'mechanisms']

    def get_mechanisms(self, obj):
        items = obj.categorymechanism_set.all()
        return CategoryMechanismSerializer(items, many=True).data


class CasingCategorySerializer(serializers.ModelSerializer):
    children = CategoryRecursiveField(many=True)

    class Meta:
        model = Category
        fields = ['name', 'slug', 'children']


class BreadcrumbSerializer(serializers.ModelSerializer):
    parent_category = ProductCategoryRecursiveField()

    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent_category']


def count_child_category_products(category):
    products_count = category.product_set.count()
    if category.children:
        for child in category.children.all():
            products_count = products_count + count_child_category_products(child)
    return products_count


class HomeCategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['img_thumb', 'slug', 'name', 'products_count']

    def get_products_count(self, obj):
        return count_child_category_products(obj)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        exclude = ['id']


class ProductCategorySerializer(serializers.ModelSerializer):
    parent_category = ProductCategoryRecursiveField()

    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent_category']
        depth=5


class CasingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Casing
        fields = ['name', 'img_thumb', 'id']


class FrameMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameMaterial
        exclude = ['id']


class UpholsteryMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpholsteryMaterial
        exclude = ['id']


class FillerMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = FillerMaterial
        exclude = ['id']


class SupportMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportMaterial
        exclude = ['id']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['name', 'img_thumb', 'id']


class SimilarProductsSerializer(serializers.ModelSerializer):
    product_img = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['catalog_name', 'price', 'old_price', 'product_img', 'slug']

    def get_product_img(self, obj):
        try:
            return str(obj.images.order_by('-priority')[0].img_thumb)
        except:
            return None


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ['id', 'product']


class ProductSerializer(serializers.ModelSerializer):
    mechanism = MechanismSerializer()
    country = CountrySerializer()
    category = ProductCategorySerializer()
    casings = CasingSerializer(many=True)
    colors = ColorSerializer(many=True)
    frame_material = FrameMaterialSerializer(many=True)
    upholstery_material = UpholsteryMaterialSerializer(many=True)
    filler_material = FillerMaterialSerializer(many=True)
    support_material = SupportMaterialSerializer(many=True)
    similar_products = SimilarProductsSerializer(many=True)
    images_set = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_images_set(self, obj):
        images = obj.images.all().order_by('-priority')
        return ProductImageSerializer(images, many=True).data


class HomeProductSerializer(serializers.ModelSerializer):
    product_img = serializers.SerializerMethodField()
    category = ProductCategorySerializer()

    class Meta:
        model = Product
        fields = ['catalog_name', 'price', 'product_img', 'category', 'slug']

    def get_product_img(self, obj):
        try:
            return str(obj.images.order_by('-priority')[0].img_thumb)
        except:
            return None


class HomeSaleProductSerializer(serializers.ModelSerializer):
    product_img = serializers.SerializerMethodField()
    category = ProductCategorySerializer()

    class Meta:
        model = Product
        fields = ['catalog_name', 'price', 'old_price', 'product_img', 'category', 'slug', 'width', 'height', 'depth']

    def get_product_img(self, obj):
        try:
            return str(obj.images.order_by('-priority')[0].img_thumb)
        except:
            return None


class DeliveryPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'delivery_price']


class LiftPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'lift_price']
