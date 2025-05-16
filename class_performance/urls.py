from django.urls import path
from . import views

app_name = 'class_performance'

urlpatterns = [
    path('', views.index, name='index'),
    path('ranking/', views.ranking_view, name='ranking'),
    path('report/', views.report_view, name='report'),
]