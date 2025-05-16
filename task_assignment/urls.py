from django.urls import path
from . import views

app_name = 'task_assignment'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    
    # Teacher URLs
    path('teacher/create_task/', views.create_task, name='create_task'),
    path('teacher/assign_task/<int:task_id>/', views.assign_task, name='assign_task'),
    path('teacher/grade_task/<int:submission_id>/', views.grade_task, name='grade_task'),
    path('teacher/view_submissions/<int:task_id>/', views.view_submissions, name='view_submissions'),

    # Student URLs
    path('student/view_tasks/', views.view_tasks, name='view_tasks'),
    path('student/submit_task/<int:assignment_id>/', views.submit_task, name='submit_task'),
    path('student/view_grades/', views.view_grades, name='view_grades'),
]