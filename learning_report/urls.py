from django.urls import path
from . import views

urlpatterns = [
    # 将 diagnosis/ 的路由定义放在前面
    path('diagnosis/', views.mistake_diagnosis, name='mistake_diagnosis'),  # 实际路径为 report/diagnosis/
    path('', views.report_home, name='report_home'),  # 实际路径为 report/
]