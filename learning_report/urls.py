from django.urls import path
from . import views

app_name = 'learning_report'

urlpatterns = [
    path('', views.view_report_list, name='report_list'),
    path('generate/', views.generate_weekly_report, name='generate_report'),
    path('generate/<str:date>/', views.generate_weekly_report, name='generate_report_date'),
    path('detail/<int:report_id>/', views.view_report_detail, name='report_detail'),
]