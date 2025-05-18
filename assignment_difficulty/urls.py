# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.analyze_difficulty, name='difficulty_analysis'),
    path('result/<int:analysis_id>/', views.analysis_result, name='analysis_result'),
]