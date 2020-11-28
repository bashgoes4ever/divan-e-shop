# coding=utf-8
from django.urls import path
from .views import *


urlpatterns = [
    path('misc/', Misc.as_view()),
]