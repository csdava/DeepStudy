from django.shortcuts import render
from django.db.models import Avg, Count
from .models import Student, Homework, Exam, ClassInteraction, StudyBehavior


def index(request):
    """班级表现主页视图"""
    return render(request, 'class_performance/index.html', {
        'title': '班级表现分析'
    })


def calculate_performance_score(student):
    # 权重分配（可调整）
    weights = {
        'homework': 0.3,
        'exam': 0.4,
        'interaction': 0.15,
        'behavior': 0.15
    }

    try:
        # 计算各项指标
        homework_avg = Homework.objects.filter(student=student).aggregate(
            avg_sub=Avg('submission_rate'),
            avg_acc=Avg('accuracy')
        )
        
        # 处理空值情况
        homework_score = 0
        if homework_avg['avg_sub'] is not None and homework_avg['avg_acc'] is not None:
            homework_score = (homework_avg['avg_sub'] * 0.4 + homework_avg['avg_acc'] * 0.6)
        
        exam_avg = Exam.objects.filter(student=student).aggregate(avg_score=Avg('score'))
        exam_score = exam_avg['avg_score'] or 0
        
        try:
            interaction = ClassInteraction.objects.get(student=student)
            interaction_score = (interaction.questions_asked * 0.3 + 
                               interaction.answers_given * 0.7 * (interaction.answer_accuracy/100)) * 10  # 标准化到100分
        except ClassInteraction.DoesNotExist:
            interaction_score = 0
        
        try:
            behavior = StudyBehavior.objects.get(student=student)
            behavior_score = (behavior.study_hours / 40 * 0.6 + behavior.resource_usage / 100 * 0.4) * 100  # 标准化到100分
        except StudyBehavior.DoesNotExist:
            behavior_score = 0

        # 综合得分计算
        score = (
            homework_score * weights['homework'] +
            exam_score * weights['exam'] +
            interaction_score * weights['interaction'] +
            behavior_score * weights['behavior']
        )

        return round(score, 2)
    except Exception as e:
        print(f"Error calculating score for student {student.name}: {str(e)}")
        return 0


def ranking_view(request):
    try:
        students = Student.objects.all()
        if not students.exists():
            return render(request, 'class_performance/ranking.html', {
                'students': [],
                'error_message': '暂无学生数据'
            })

        ranked_students = []

        for student in students:
            score = calculate_performance_score(student)
            ranked_students.append({
                'name': student.name,
                'score': score,
                'id': student.student_id
            })

        # 按分数降序排列
        ranked_students.sort(key=lambda x: x['score'], reverse=True)

        # 添加排名
        for i, student in enumerate(ranked_students, 1):
            student['rank'] = i

        return render(request, 'class_performance/ranking.html', {'students': ranked_students})
    except Exception as e:
        print(f"Error in ranking view: {str(e)}")
        return render(request, 'class_performance/ranking.html', {
            'error_message': '生成排行榜时发生错误'
        })


def generate_class_report():
    try:
        # 班级整体数据分析
        total_students = Student.objects.count()
        
        if total_students == 0:
            return {
                'total_students': 0,
                'homework_sub': 0,
                'homework_acc': 0,
                'exam_avg': 0,
                'questions_avg': 0,
                'answers_avg': 0,
                'study_hours': 0,
                'resource_usage': 0,
                'error_message': '暂无学生数据'
            }

        homework_stats = Homework.objects.aggregate(
            avg_sub=Avg('submission_rate'),
            avg_acc=Avg('accuracy')
        )

        exam_stats = Exam.objects.aggregate(avg_score=Avg('score'))

        interaction_stats = ClassInteraction.objects.aggregate(
            avg_questions=Avg('questions_asked'),
            avg_answers=Avg('answers_given'),
            avg_accuracy=Avg('answer_accuracy')
        )

        behavior_stats = StudyBehavior.objects.aggregate(
            avg_hours=Avg('study_hours'),
            avg_usage=Avg('resource_usage')
        )

        return {
            'total_students': total_students,
            'homework_sub': round(homework_stats['avg_sub'] or 0, 2),
            'homework_acc': round(homework_stats['avg_acc'] or 0, 2),
            'exam_avg': round(exam_stats['avg_score'] or 0, 2),
            'questions_avg': round(interaction_stats['avg_questions'] or 0, 1),
            'answers_avg': round(interaction_stats['avg_answers'] or 0, 1),
            'answer_accuracy': round(interaction_stats['avg_accuracy'] or 0, 1),
            'study_hours': round(behavior_stats['avg_hours'] or 0, 1),
            'resource_usage': round(behavior_stats['avg_usage'] or 0, 1)
        }
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        return {
            'error_message': '生成报告时发生错误',
            'total_students': 0,
            'homework_sub': 0,
            'homework_acc': 0,
            'exam_avg': 0,
            'questions_avg': 0,
            'answers_avg': 0,
            'study_hours': 0,
            'resource_usage': 0
        }


def report_view(request):
    try:
        report_data = generate_class_report()
        return render(request, 'class_performance/report.html', {'report': report_data})
    except Exception as e:
        print(f"Error in report view: {str(e)}")
        return render(request, 'class_performance/report.html', {
            'report': {
                'error_message': '生成报告时发生错误'
            }
        })