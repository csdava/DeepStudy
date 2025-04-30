from django.db import models

# Create your models here.
class GeneratedTest(models.Model):
    """
    AI生成测试题记录
    """
    student = models.ForeignKey('user_management.UserProfile', on_delete=models.CASCADE)
    base_content = models.TextField(verbose_name="原始内容参考")
    generated_questions = models.JSONField(verbose_name="生成试题")
    difficulty_level = models.FloatField(verbose_name="难度系数")
    generation_date = models.DateTimeField(auto_now_add=True)