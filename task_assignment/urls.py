from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='task_index'),
    path('teacher/tasks/', views.task_list, name='task_list'),
    path('teacher/tasks/create/', views.task_create, name='task_create'),
    path('teacher/tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('teacher/tasks/<int:task_id>/assign/', views.task_assign, name='task_assign'),
    path('student/tasks/', views.student_task_list, name='student_task_list'),
    path('student/tasks/<int:assignment_id>/submit/', views.task_submit, name='task_submit'),
]