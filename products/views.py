from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import *
from django.core.paginator import Paginator
from django.db.models import Max, Min


def get_parent_category(category):
    if category.parent_category:
        return get_parent_category(category.parent_category)
    else:
        return category


class Categories(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        slug = request.GET.get('slug', None)
        if slug:
            obj = get_parent_category(Category.objects.get(slug=slug))
            serializer = CategorySerializer(obj)
            return Response(serializer.data)
        else:
            objs = Category.objects.filter(level=0)
            serializer = CategorySerializer(objs, many=True)
            return Response(serializer.data)


class CasingCategories(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        objs = CasingCategory.objects.filter(level=0)
        serializer = CasingCategorySerializer(objs, many=True)
        return Response(serializer.data)


class CasingBreadcrumbs(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        slug = request.GET.get('category', None)
        if slug:
            obj = CasingCategory.objects.get(slug=slug)
            serializer = BreadcrumbSerializer(obj)
            return Response(serializer.data)
        return Response({"error": "slug not provided"})


class Breadcrumbs(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        slug = request.GET.get('slug', None)
        if slug:
            obj = Category.objects.get(slug=slug)
            serializer = BreadcrumbSerializer(obj)
            return Response(serializer.data)
        return Response({"error": "slug not provided"})


class DeliveryPrices(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        objs = Category.objects.filter(delivery_price__isnull=False)
        serializer = DeliveryPriceSerializer(objs, many=True)
        return Response(serializer.data)


class LiftPrices(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        objs = Category.objects.filter(lift_price__isnull=False)
        serializer = LiftPriceSerializer(objs, many=True)
        return Response(serializer.data)


class HomeCategories(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        objs = Category.objects.filter(is_main=True)
        serializer = HomeCategorySerializer(objs, many=True)
        return Response(serializer.data)


class Products(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, slug=None):
        if slug:
            objs = Product.objects.get(slug=slug)
            serializer = ProductSerializer(objs, many=False)
            return Response(serializer.data)
        else:
            objs = Product.objects.all()
            serializer = ProductSerializer(objs, many=True)
            return Response(serializer.data)


class HomeProducts(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        objs = Product.objects.all().order_by('-priority')
        paginator = Paginator(objs, request.GET.get('items', 6))
        page_num = request.GET.get('page', 1)
        objs_paginated = paginator.get_page(page_num)
        serializer = HomeProductSerializer(objs_paginated, many=True)
        page_next = objs_paginated.next_page_number() if objs_paginated.has_next() else 0
        return Response({
            'data': serializer.data,
            'next_page': page_next,
            'has_next': objs_paginated.has_next(),
            'has_prev': objs_paginated.has_previous(),
            'count': paginator.num_pages,
            'current_page': request.GET.get('page', 1)
        })


class HomeSaleProducts(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        objs = Product.objects.filter(old_price__isnull=False).order_by('-priority')
        paginator = Paginator(objs, request.GET.get('items', 6))
        page_num = request.GET.get('page', 1)
        objs_paginated = paginator.get_page(page_num)
        serializer = HomeSaleProductSerializer(objs_paginated, many=True)
        page_next = objs_paginated.next_page_number() if objs_paginated.has_next() else 0
        return Response({
            'data': serializer.data,
            'next_page': page_next,
            'has_next': objs_paginated.has_next(),
            'has_prev': objs_paginated.has_previous(),
            'count': paginator.num_pages,
            'current_page': request.GET.get('page', 1)
        })


def get_child_category_ids(category, res=None):
    if res is None:
        res = [category.id]
    if len(category.children.all()) > 0:
        for child in category.children.all():
            res.append(child.id)
            get_child_category_ids(child, res)
    return res


class CatalogProducts(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # order
        order = request.GET.get('order', None)
        order_by = '-priority'
        if order == 'prices_up':
            order_by = 'price'
        elif order == 'prices_down':
            order_by = '-price'

        # filters
        filters = {}
        if request.GET.get('min_price'):
            filters['price__gte'] = request.GET.get('min_price')
        if request.GET.get('max_price'):
            filters['price__lte'] = request.GET.get('max_price')
        if request.GET.get('min_width'):
            filters['width__gte'] = request.GET.get('min_width')
        if request.GET.get('max_width'):
            filters['width__lte'] = request.GET.get('max_width')
        if request.GET.get('min_height'):
            filters['height__gte'] = request.GET.get('min_height')
        if request.GET.get('max_height'):
            filters['height__lte'] = request.GET.get('max_height')
        if request.GET.get('mechanisms'):
            filters['mechanism_id__in'] = request.GET.getlist('mechanisms')

        # get category
        category = Category.objects.get(slug=request.GET.get('category', None)) if request.GET.get('category', None) else None
        if not category:
            filters['old_price__isnull'] = False

        if category and category.children:
            categories = get_child_category_ids(category)
            filters['category_id__in'] = categories
            objs = Product.objects.filter(**filters).order_by(order_by)
        else:
            if category:
                filters['category'] = category
                objs = Product.objects.filter(**filters).order_by(order_by)
            else:
                objs = Product.objects.filter(**filters).order_by(order_by)


        paginator = Paginator(objs, request.GET.get('items', 6))
        page_num = request.GET.get('page', 1)
        objs_paginated = paginator.get_page(page_num)
        serializer = HomeSaleProductSerializer(objs_paginated, many=True)
        page_next = objs_paginated.next_page_number() if objs_paginated.has_next() else 0
        return Response({
            'data': serializer.data,
            'next_page': page_next,
            'has_next': objs_paginated.has_next(),
            'has_prev': objs_paginated.has_previous(),
            'count': paginator.num_pages,
            'current_page': request.GET.get('page', 1)
        })


class CasingCatalogProducts(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):

        # filters
        filters = {}

        # get category
        category = CasingCategory.objects.get(slug=request.GET.get('category', None)) if request.GET.get('category', None) else None

        if category and category.children:
            categories = get_child_category_ids(category)
            filters['category_id__in'] = categories
            objs = Casing.objects.filter(**filters)
        else:
            if category:
                filters['category'] = category
                objs = Casing.objects.filter(**filters)
            else:
                objs = Casing.objects.filter(**filters)

        serializer = CasingSerializer(objs, many=True)
        return Response(serializer.data)


class CatalogMenu(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        category = Category.objects.get(slug=request.GET.get('category', None))
        if category.children:
            categories = get_child_category_ids(category)
            objs = Product.objects.filter(category_id__in=categories)
            mechanisms = CategoryMechanism.objects.filter(category=category)
        else:
            objs = Product.objects.filter(category=category)
            mechanisms = CategoryMechanism.objects.filter(category=category)
        min_price = objs.aggregate(Min('price'))['price__min']
        max_price = objs.aggregate(Max('price'))['price__max']
        min_width = objs.aggregate(Min('width'))['width__min']
        max_width = objs.aggregate(Max('width'))['width__max']
        min_height = objs.aggregate(Min('height'))['height__min']
        max_height = objs.aggregate(Max('height'))['height__max']
        serializer = CategoryMechanismSerializer(mechanisms, many=True)

        return Response({
            "min_price": min_price,
            "max_price": max_price,
            "min_width": min_width,
            "max_width": max_width,
            "min_height": min_height,
            "max_height": max_height,
            "mechanisms": serializer.data
        })