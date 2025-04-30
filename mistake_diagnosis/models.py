from django.db import models

# Create your models here.
class MistakeRecord(models.Model):
    """
    学生错题诊断记录
    """
    student = models.ForeignKey('user_management.UserProfile', on_delete=models.CASCADE)
    original_question = models.TextField(verbose_name="原题内容")
    analysis_result = models.JSONField(verbose_name="错题分析")
    suggested_resources = models.ManyToManyField('resource_library.Resource')
    diagnosed_at = models.DateTimeField(auto_now_add=True)