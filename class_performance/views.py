from django.shortcuts import render
from .models import Student, Homework, Exam, LearningBehavior
import matplotlib.pyplot as plt
import io
import base64

def calculate_student_score(student):
    homeworks = Homework.objects.filter(student=student)
    exams = Exam.objects.filter(student=student)
    behaviors = LearningBehavior.objects.filter(student=student)

    # 计算作业得分
    homework_score = 0
    if homeworks:
        total_score = 0
        for hw in homeworks:
            if hw.score is not None:
                total_score += hw.score
        homework_score = total_score / len(homeworks)

    # 计算考试得分
    exam_score = 0
    if exams:
        total_score = 0
        for exam in exams:
            if exam.score is not None:
                total_score += exam.score
        exam_score = total_score / len(exams)

    # 计算学习行为得分
    behavior_score = 0
    if behaviors:
        total_participation = 0
        total_completion = 0
        for behavior in behaviors:
            total_participation += behavior.participation_score
            total_completion += behavior.homework_completion
        behavior_score = (total_participation / len(behaviors) * 0.6 + 
                         total_completion / len(behaviors) * 0.4)

    # 计算最终得分
    return homework_score * 0.4 + exam_score * 0.4 + behavior_score * 0.2

def get_student_ranking():
    students = Student.objects.all()
    student_scores = {student: calculate_student_score(student) for student in students}
    sorted_students = sorted(student_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_students

def index(request):
    student_ranking = get_student_ranking()
    context = {'student_ranking': student_ranking}
    return render(request, 'class_performance/index.html', context)

def charts(request):
    student_ranking = get_student_ranking()
    scores = [score for _, score in student_ranking]

    # Generate bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(scores)), scores, tick_label=[student.name for student, _ in student_ranking])
    plt.xlabel('Students')
    plt.ylabel('Scores')
    plt.title('Student Performance Scores')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    bar_chart = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    # Generate line chart
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(scores)), scores, marker='o')
    plt.xlabel('Students')
    plt.ylabel('Scores')
    plt.title('Student Performance Trends')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    line_chart = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    context = {'bar_chart': bar_chart, 'line_chart': line_chart}
    return render(request, 'class_performance/charts.html', context)

def report(request):
    student_ranking = get_student_ranking()
    top_students = student_ranking[:3]
    bottom_students = student_ranking[-3:]

    if student_ranking:
        average_score = sum([score for _, score in student_ranking]) / len(student_ranking)
    else:
        average_score = 0

    context = {
        'top_students': top_students,
        'bottom_students': bottom_students,
        'average_score': average_score
    }
    return render(request, 'class_performance/report.html', context)