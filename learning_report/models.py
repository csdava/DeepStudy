# models.py（新增错题诊断相关模型）
from django.db import models

class MistakeDiagnosis(models.Model):
    """
    错题诊断记录
    """
    student = models.ForeignKey('user_management.UserProfile', on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, verbose_name="学科")
    knowledge_point = models.CharField(max_length=100, verbose_name="知识点")
    original_question = models.JSONField(verbose_name="原始题目数据")
    student_answer = models.TextField(verbose_name="学生答案")
    self_analysis = models.TextField(blank=True, verbose_name="自我分析")
    diagnosis_result = models.JSONField(verbose_name="诊断结果")
    created_at = models.DateTimeField(auto_now_add=True)

class SimilarQuestion(models.Model):
    """
    相似题目库
    """
    subject = models.CharField(max_length=50)
    knowledge_points = models.CharField(max_length=200)
    question_text = models.TextField()
    answer = models.TextField()
    solution = models.TextField()
    difficulty = models.CharField(max_length=20)
    source = models.CharField(max_length=100, blank=True)