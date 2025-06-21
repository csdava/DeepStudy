"""
URL configuration for DjangoProject3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from user_management import views as user_views
from django.views.generic import RedirectView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests
import logging
from class_management.views import proxy_to_flask

logger = logging.getLogger(__name__)

def redirect_to_testgen(request):
    return redirect('test_generator_index')

urlpatterns = [
    path('', user_views.role_selection, name='role_selection'),  # 新的首页为身份选择
    path('admin/', admin.site.urls),
    
    # 身份登录和注册相关
    path('teacher/login/', user_views.teacher_login, name='teacher_login'),
    path('student/login/', user_views.student_login, name='student_login'),
    path('teacher/register/', user_views.teacher_register, name='teacher_register'),
    path('student/register/', user_views.student_register, name='student_register'),
    path('teacher/dashboard/', user_views.teacher_dashboard, name='teacher_dashboard'),
    path('student/dashboard/', user_views.student_dashboard, name='student_dashboard'),
    path('logout/', user_views.user_logout, name='logout'),  # 使用自定义的登出视图
    
    # 教师功能模块
    path('class_performance/', include('class_performance.urls')),
    path('lessons/', include('lesson_plan_generator.urls')),
    path('class_management/', include('class_management.urls', namespace='class_management')),
    path('task_assignment/', include('task_assignment.urls')),
    path('assignment/', include('assignment_difficulty.urls')),
    
    # 学生功能模块
    path('testgen/', include('test_generator.urls')),
    path('report/', include('learning_report.urls', namespace='learning_report')),
    path('diagnosis/', include('mistake_diagnosis.urls', namespace='mistake_diagnosis')),
    path('learning-path/', include('learning_path_recommendation.urls', namespace='learning_path')),
    
    # 错题管理相关
    path('problem/<uuid:problem_id>/', proxy_to_flask, name='problem_detail'),
    path('error_management/', proxy_to_flask, name='error_management'),
    path('error_management/<path:path>', proxy_to_flask, name='error_management_path'),
    path('api/<path:path>', proxy_to_flask, name='api_proxy'),
    path('uploads/<path:path>', proxy_to_flask, name='uploads_proxy'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 添加media文件服务