from django.urls import path
from . import views

app_name = 'class_performance'

urlpatterns = [
    path('', views.performance_dashboard, name='dashboard'),
    path('get_students/', views.get_students, name='get_students'),
    path('get_class_performance/', views.get_class_performance, name='get_class_performance'),
    path('get_student_performance/', views.get_student_performance, name='get_student_performance'),
]
