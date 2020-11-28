# coding=utf-8
from django.urls import path
from .views import *


urlpatterns = [
    path('categories/', Categories.as_view()),
    path('breadcrumbs/', Breadcrumbs.as_view()),
    path('home/categories/', HomeCategories.as_view()),
    path('home/products/', HomeProducts.as_view()),
    path('home/sale-products/', HomeSaleProducts.as_view()),
    path('products/', Products.as_view()),
    path('products/<str:slug>', Products.as_view()),
    path('catalog/products/', CatalogProducts.as_view()),
    path('catalog/menu/', CatalogMenu.as_view()),
    path('delivery-prices/', DeliveryPrices.as_view()),
    path('lift-prices/', LiftPrices.as_view()),
    path('casing-categories/', CasingCategories.as_view()),
    path('casing-breadcrumbs/', CasingBreadcrumbs.as_view()),
    path('casings/', CasingCatalogProducts.as_view()),
]