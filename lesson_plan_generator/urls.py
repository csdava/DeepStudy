# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lesson_plan_list, name='lesson_list'),
    path('new/', views.generate_lesson_plan, name='create_lesson'),
    path('<int:pk>/', views.lesson_plan_detail, name='lesson_detail'),
    path('<int:pk>/edit/', views.edit_lesson_plan, name='edit_lesson'),
    path('<int:pk>/share/', views.share_lesson, name='share_lesson'),
]