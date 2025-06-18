from django.shortcuts import render, redirect, get_object_or_404
from .models import Class, Student, Activity
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import logging
from wsgiref.util import FileWrapper
import io

logger = logging.getLogger(__name__)

# 班级信息展示页面
def class_info(request):
    classes = Class.objects.all()
    return render(request, 'class_management/class_info.html', {'classes': classes})

# 创建班级
def create_class(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        grade = request.POST.get('grade')
        subject = request.POST.get('subject')
        Class.objects.create(name=name, grade=grade, subject=subject)
        messages.success(request, '班级创建成功！')
        return redirect('class_management:class_info')
    return render(request, 'class_management/create_class.html')

# 编辑班级
def edit_class(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        class_obj.name = request.POST.get('name')
        class_obj.grade = request.POST.get('grade')
        class_obj.subject = request.POST.get('subject')
        class_obj.save()
        messages.success(request, '班级信息更新成功！')
        return redirect('class_management:class_info')
    return render(request, 'class_management/edit_class.html', {'class': class_obj})

# 删除班级
def delete_class(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        class_obj.delete()
        messages.success(request, '班级已删除！')
        return redirect('class_management:class_info')
    return render(request, 'class_management/delete_class.html', {'class': class_obj})

# 学生名单管理页面
def student_list(request, class_id):
    class_info = get_object_or_404(Class, id=class_id)
    students = class_info.students.all()
    return render(request, 'class_management/student_list.html', {'class_info': class_info, 'students': students})

# 添加学生
def add_student(request, class_id):
    class_info = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        student_id = request.POST.get('student_id')
        Student.objects.create(name=name, student_id=student_id, class_info=class_info)
        messages.success(request, '学生添加成功！')
        return redirect('class_management:student_list', class_id=class_id)
    return render(request, 'class_management/add_student.html', {'class_info': class_info})

# 编辑学生信息
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.student_id = request.POST.get('student_id')
        student.save()
        messages.success(request, '学生信息更新成功！')
        return redirect('class_management:student_list', class_id=student.class_info.id)
    return render(request, 'class_management/edit_student.html', {'student': student})

# 删除学生
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    class_id = student.class_info.id
    if request.method == 'POST':
        student.delete()
        messages.success(request, '学生已删除！')
        return redirect('class_management:student_list', class_id=class_id)
    return render(request, 'class_management/delete_student.html', {'student': student})

# 活动管理页面
def activity_list(request, class_id):
    class_info = get_object_or_404(Class, id=class_id)
    activities = class_info.activities.all()
    return render(request, 'class_management/activity_list.html', {'class_info': class_info, 'activities': activities})

# 创建活动
def create_activity(request, class_id):
    class_info = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        time = request.POST.get('time')
        location = request.POST.get('location')
        activity = Activity.objects.create(
            name=name,
            time=time,
            location=location,
            class_info=class_info
        )
        selected_students = request.POST.getlist('participants')
        activity.participants.set(selected_students)
        messages.success(request, '活动创建成功！')
        return redirect('class_management:activity_list', class_id=class_id)
    students = class_info.students.all()
    return render(request, 'class_management/create_activity.html', {
        'class_info': class_info,
        'students': students
    })

# 编辑活动
def edit_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    if request.method == 'POST':
        activity.name = request.POST.get('name')
        activity.time = request.POST.get('time')
        activity.location = request.POST.get('location')
        activity.save()
        selected_students = request.POST.getlist('participants')
        activity.participants.set(selected_students)
        messages.success(request, '活动信息更新成功！')
        return redirect('class_management:activity_list', class_id=activity.class_info.id)
    students = activity.class_info.students.all()
    return render(request, 'class_management/edit_activity.html', {
        'activity': activity,
        'students': students
    })

# 删除活动
def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    class_id = activity.class_info.id
    if request.method == 'POST':
        activity.delete()
        messages.success(request, '活动已删除！')
        return redirect('class_management:activity_list', class_id=class_id)
    return render(request, 'class_management/delete_activity.html', {'activity': activity})

# 权限设置页面
def permission_settings(request, class_id):
    class_info = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        class_info.permission_view_scores = request.POST.get('permission_view_scores') == 'on'
        deadline = request.POST.get('homework_deadline')
        if deadline:
            class_info.homework_deadline = deadline
        class_info.save()
        messages.success(request, '权限设置已更新！')
        return redirect('class_management:class_info')
    return render(request, 'class_management/permission_settings.html', {'class_info': class_info})

@csrf_exempt  # 添加CSRF豁免装饰器
def proxy_to_flask(request, path=''):
    """
    Proxy view to forward requests to Flask application
    """
    # 记录原始请求信息
    logger.info(f"Original request path: {request.path}")
    logger.info(f"Original request method: {request.method}")
    logger.info(f"Request headers: {dict(request.headers)}")
    
    # 处理请求路径
    if request.path.startswith('/api/'):
        # API请求
        path_suffix = request.path[len('/api/'):]  # 移除 '/api/' 前缀
        flask_url = f'http://localhost:5001/api/{path_suffix}'
    elif request.path.startswith('/error_management/api/'):
        # 带前缀的API请求
        path_suffix = request.path[len('/error_management/api/'):]  # 移除 '/error_management/api/' 前缀
        flask_url = f'http://localhost:5001/api/{path_suffix}'
    elif request.path.startswith('/error_management/static/'):
        # 静态资源请求
        path_suffix = request.path[len('/error_management/static/'):]  # 移除 '/error_management/static/' 前缀
        flask_url = f'http://localhost:5001/static/{path_suffix}'
    elif request.path.startswith('/uploads/'):
        # 上传图片请求
        path_suffix = request.path[len('/uploads/'):]  # 移除 '/uploads/' 前缀
        flask_url = f'http://localhost:5001/uploads/{path_suffix}'
    elif request.path.startswith('/problem/'):
        # 错题详情请求
        problem_id = request.path.split('/')[-2]  # 获取problem_id
        flask_url = f'http://localhost:5001/problem/{problem_id}'
    elif request.path.startswith('/error_management/'):
        # 普通页面请求
        path_suffix = request.path[len('/error_management/'):]
        flask_url = f'http://localhost:5001/{path_suffix}'
    else:
        # 其他未捕获的路径，直接转发（例如根路径 '/' 如果Flask也处理它）
        flask_url = f'http://localhost:5001{request.path}'
    
    logger.info(f"Proxying to Flask URL: {flask_url}")
    
    # Forward the request method and headers
    headers = {key: value for key, value in request.headers.items() 
              if key.lower() not in ['host', 'content-length', 'connection', 'keep-alive', 'proxy-authenticate',
                                   'proxy-authorization', 'te', 'trailers', 'transfer-encoding', 'upgrade']}
    
    # 处理请求数据
    data = None
    if request.method in ['POST', 'PUT', 'PATCH']:
        if request.content_type and 'application/json' in request.content_type:
            try:
                data = json.loads(request.body)
                logger.info(f"Request JSON data: {data}")
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {str(e)}")
                data = request.POST.dict()
        else:
            data = request.POST.dict()
            logger.info(f"Request form data: {data}")
    
    # Forward the request to Flask
    try:
        # Use stream=True to handle large responses
        response = requests.request(
            method=request.method,
            url=flask_url,
            headers=headers,
            json=data if request.method in ['POST', 'PUT', 'PATCH'] else None,
            data=request.body if request.method not in ['POST', 'PUT', 'PATCH'] else None,
            cookies=request.COOKIES,
            allow_redirects=False,
            timeout=30,  # Increased timeout
            stream=True  # Enable streaming
        )
        
        logger.info(f"Flask response status: {response.status_code}")
        content_type = response.headers.get('Content-Type', 'unknown').lower()
        logger.info(f"Flask response Content-Type: {content_type}")

        # 记录API响应内容
        if 'application/json' in content_type:
            try:
                response_data = response.json()
                logger.info(f"Flask JSON response: {response_data}")
            except json.JSONDecodeError:
                logger.error("Failed to decode JSON response")

        # Handle binary responses (images, files, etc.)
        if any(content_type.startswith(prefix) for prefix in ['image/', 'application/octet-stream', 'application/pdf']):
            # Use StreamingHttpResponse for binary content
            django_response = StreamingHttpResponse(
                streaming_content=response.iter_content(chunk_size=8192),
                content_type=content_type
            )
        else:
            # For non-binary content, process as before
            content = response.content
            if 'text/html' in content_type:
                content = content.decode('utf-8')
                # 替换所有可能的静态资源路径
                replacements = [
                    # CSS文件
                    ('href="/static/', 'href="/error_management/static/'),
                    ('href=\'/static/', 'href=\'/error_management/static/'),
                    # JavaScript文件
                    ('src="/static/', 'src="/error_management/static/'),
                    ('src=\'/static/', 'src=\'/error_management/static/'),
                    # CSS中的URL
                    ('url("/static/', 'url("/error_management/static/'),
                    ('url(\'/static/', 'url(\'/error_management/static/'),
                    ('url( "/static/', 'url( "/error_management/static/'),
                    ('url( \'/static/', 'url(\'/error_management/static/'),
                    # API路径
                    ('action="/api/', 'action="/error_management/api/'),
                    ('fetch("/api/', 'fetch("/error_management/api/'),
                    ('url: "/api/', 'url: "/error_management/api/'),
                    ('"/api/', '"/error_management/api/'),  # 添加通用替换
                    # 其他页面路径
                    ('href="/prompt_settings"', 'href="/error_management/prompt_settings"'),
                    ('href="/api_config"', 'href="/error_management/api_config"'),
                    ('href="/review"', 'href="/error_management/review"'),
                    ('href="/problems/math"', 'href="/error_management/problems/math"'),
                    # 根路径
                    ('href="/"', 'href="/error_management/"'),
                    ('src="/"', 'src="/error_management/"'),
                    # 其他可能的路径
                    ('href="static/', 'href="/error_management/static/'),
                    ('src="static/', 'src="/error_management/static/'),
                    ('url("static/', 'url("/error_management/static/'),
                    ('url(\'static/', 'url(\'/error_management/static/'),
                    # 图片上传路径
                    ('src="/uploads/', 'src="/error_management/uploads/'),
                    # 错题详情路径
                    ('href="/problem/', 'href="/error_management/problem/'),
                    ('src="/problem/', 'src="/error_management/problem/'),
                ]
                
                for old, new in replacements:
                    content = content.replace(old, new)
                
                content = content.encode('utf-8')
            
            django_response = HttpResponse(
                content=content,
                status=response.status_code,
                content_type=content_type
            )
        
        # Copy headers from Flask response, excluding hop-by-hop headers
        for key, value in response.headers.items():
            if key.lower() not in ['content-length', 'content-encoding', 'connection', 'keep-alive',
                                 'proxy-authenticate', 'proxy-authorization', 'te', 'trailers',
                                 'transfer-encoding', 'upgrade']:
                django_response[key] = value
                
        return django_response
    except requests.RequestException as e:
        logger.error(f"Error connecting to Flask: {str(e)}")
        # 处理请求异常
        return HttpResponse(
            content=json.dumps({
                'error': 'Error connecting to error management service',
                'details': str(e)
            }),
            status=503,
            content_type='application/json'
        )