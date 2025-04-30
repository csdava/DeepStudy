from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),  # 直接指向视图函数，不再 include 其他模块
]