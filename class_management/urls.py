from django.urls import path
from . import views

app_name = 'class_management'

urlpatterns = [
    # 班级管理
    path('', views.class_info, name='class_info'),
    path('create/', views.create_class, name='create_class'),
    path('edit/<int:class_id>/', views.edit_class, name='edit_class'),
    path('delete/<int:class_id>/', views.delete_class, name='delete_class'),
    
    # 学生管理
    path('class/<int:class_id>/students/', views.student_list, name='student_list'),
    path('class/<int:class_id>/students/add/', views.add_student, name='add_student'),
    path('student/<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('student/<int:student_id>/delete/', views.delete_student, name='delete_student'),
    
    # 活动管理
    path('class/<int:class_id>/activities/', views.activity_list, name='activity_list'),
    path('class/<int:class_id>/activities/create/', views.create_activity, name='create_activity'),
    path('activity/<int:activity_id>/edit/', views.edit_activity, name='edit_activity'),
    path('activity/<int:activity_id>/delete/', views.delete_activity, name='delete_activity'),
    
    # 权限管理
    path('class/<int:class_id>/permissions/', views.permission_settings, name='permission_settings'),
]