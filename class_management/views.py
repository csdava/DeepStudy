from django.shortcuts import render, redirect, get_object_or_404
from .models import Class, Student, Activity
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone

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