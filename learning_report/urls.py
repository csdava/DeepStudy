from django.urls import path
from . import views

app_name = 'learning_report'

urlpatterns = [
    path('', views.report_view, name='report'),
    path('list/', views.report_list_view, name='report_list'),
]
