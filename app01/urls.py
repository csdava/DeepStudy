from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index),  # 直接指向视图函数，不再 include 其他模块
]