from django.urls import path
from . import views

urlpatterns = [
    path('learning-path/', views.learning_path_recommendation, name='learning_path'),

    path('', views.redirect_to_form, name='root_redirect'),  # 使用正确视图函数
]

