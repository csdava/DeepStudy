from django.db import models

# Create your models here.
class DifficultyAnalysis(models.Model):
    """
    AI作业难度分析记录
    """
    assignment = models.OneToOneField('task_assignment.Assignment', on_delete=models.CASCADE)
    parameters = models.JSONField(verbose_name="分析参数")
    result = models.JSONField(verbose_name="分析结果")
    created_at = models.DateTimeField(auto_now_add=True)
    accuracy_feedback = models.FloatField(verbose_name="教师反馈准确率", null=True)