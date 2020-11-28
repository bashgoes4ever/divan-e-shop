# coding=utf-8
from django.urls import path
from .views import *


urlpatterns = [
    path('basket/product/', ProductsInBasket.as_view()),
    path('basket/product/<int:id>', ProductsInBasket.as_view()),
    path('basket/', BasketView.as_view()),
]