from django.urls import path
from . import views

app_name = 'learning_path'

urlpatterns = [
    path('', views.learning_path_recommendation, name='index'),
]

