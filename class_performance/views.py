from django.shortcuts import render
from django.http import JsonResponse
from class_management.models import Class, Student
from .models import Exam, Score
import random
from django.db.models import Avg
import json
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def performance_dashboard(request):
    """成绩展示主页面"""
    classes = Class.objects.all()
    return render(request, 'class_performance/dashboard.html', {'classes': classes})

@csrf_exempt
def get_students(request):
    """获取指定班级的学生列表"""
    class_id = request.GET.get('class_id')
    students = Student.objects.filter(class_info_id=class_id).values('id', 'name')
    return JsonResponse({'students': list(students)})

@csrf_exempt
def get_class_performance(request):
    """获取班级整体成绩数据"""
    class_id = request.GET.get('class_id')
    print(f"Getting class performance for class_id: {class_id}")  # 调试信息
    
    exams = Exam.objects.filter(class_info_id=class_id).order_by('exam_date')
    
    # 如果没有考试数据，生成模拟数据
    if not exams.exists():
        print("No exams found, generating mock data")  # 调试信息
        exams = generate_mock_exams(class_id)
    
    data = {
        'dates': [],
        'scores': []
    }
    
    for exam in exams:
        avg_score = Score.objects.filter(exam=exam).aggregate(Avg('score'))['score__avg']
        if avg_score is None:
            avg_score = random.uniform(60, 100)
        data['dates'].append(exam.exam_date.strftime('%Y-%m-%d'))
        data['scores'].append(float(avg_score))
    
    print(f"Returning data: {data}")  # 调试信息
    return JsonResponse(data)

@csrf_exempt
def get_student_performance(request):
    """获取学生个人成绩数据"""
    student_id = request.GET.get('student_id')
    print(f"Getting student performance for student_id: {student_id}")  # 调试信息
    
    scores = Score.objects.filter(student_id=student_id).select_related('exam').order_by('exam__exam_date')
    
    # 如果没有成绩数据，生成模拟数据
    if not scores.exists():
        print("No scores found, generating mock data")  # 调试信息
        scores = generate_mock_scores(student_id)
    
    data = {
        'dates': [],
        'scores': []
    }
    
    for score in scores:
        data['dates'].append(score.exam.exam_date.strftime('%Y-%m-%d'))
        data['scores'].append(float(score.score))
    
    print(f"Returning data: {data}")  # 调试信息
    return JsonResponse(data)

def generate_mock_exams(class_id):
    """生成模拟考试数据"""
    class_obj = Class.objects.get(id=class_id)
    exams = []
    base_date = datetime.now()
    
    for i in range(5):  # 生成5次考试数据
        exam_date = base_date - timedelta(days=30 * (4-i))  # 从4个月前开始，每月一次考试
        exam = Exam.objects.create(
            name=f'第{i+1}次考试',
            exam_date=exam_date,
            class_info=class_obj
        )
        exams.append(exam)
        
        # 为每个学生生成成绩
        students = Student.objects.filter(class_info=class_obj)
        for student in students:
            Score.objects.create(
                exam=exam,
                student=student,
                score=random.uniform(60, 100)
            )
    return exams

def generate_mock_scores(student_id):
    """生成模拟学生成绩数据"""
    student = Student.objects.get(id=student_id)
    scores = []
    base_date = datetime.now()
    
    for i in range(5):  # 生成5次考试数据
        exam_date = base_date - timedelta(days=30 * (4-i))  # 从4个月前开始，每月一次考试
        exam = Exam.objects.create(
            name=f'第{i+1}次考试',
            exam_date=exam_date,
            class_info=student.class_info
        )
        score = Score.objects.create(
            exam=exam,
            student=student,
            score=random.uniform(60, 100)
        )
        scores.append(score)
    return scores
