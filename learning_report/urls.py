from django.urls import path
from . import views

app_name = 'learning_report'

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('all/', views.list_all_weekly_reports, name='all_reports'),
    path('generate/', views.generate_weekly_report, name='generate_report'),
    path('generate/<str:date>/', views.generate_weekly_report, name='generate_report_date'),
    path('detail/<int:report_id>/', views.view_report_detail, name='report_detail'),
]