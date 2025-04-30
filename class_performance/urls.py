from django.urls import path
from . import views

urlpatterns = [
    path('ranking/', views.ranking_view, name='ranking'),
    path('report/', views.report_view, name='report'),
]