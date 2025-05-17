# test_generator/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='test_generator_index'),
    path('generate/', views.generate_test, name='generate_test'),
    path('test/<str:uuid>/', views.test_preview, name='test_preview'),
]