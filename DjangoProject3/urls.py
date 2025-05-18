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

def redirect_to_testgen(request):
    return redirect('test_generator_index')
from django.urls import path, include
from app01 import views

urlpatterns = [
    path('', views.index, name='home'),  # Add root URL pattern
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # 添加认证URL
    path('app01/', include('app01.urls')),
    path('class_management/', include('class_management.urls', namespace='class_management')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='test_generator_index'), name='logout'),
    path('app01/', include('app01.urls')),  # 使用非空路径前缀
    path('learning-path/', include('learning_path_recommendation.urls')),
    path('report/', include('learning_report.urls')),
    path('report/diagnosis/', include('learning_report.urls')),
    path('testgen/', include('test_generator.urls')),  # 注意结尾斜杠
    path('assignment/', include('assignment_difficulty.urls')),  # 添加作业难度分析模块的URLs
    path('lessons/', include('lesson_plan_generator.urls')),  # 添加教案生成器的URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 添加media文件服务

    path('user_management/', include('user_management.urls')),
    path('task_assignment/', include('task_assignment.urls')),
    path('class_performance/', include('class_performance.urls')),
]
    # 其他路由...