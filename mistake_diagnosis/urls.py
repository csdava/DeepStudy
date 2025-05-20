from django.urls import path
from . import views

app_name = 'mistake_diagnosis'

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze/', views.analyze_mistake, name='analyze'),
    path('history/', views.history, name='history'),
] 