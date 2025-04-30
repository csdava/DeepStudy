from django.db import models

# Create your models here.
class LearningReport(models.Model):
    """
    学习周报生成记录
    """
    student = models.ForeignKey('user_management.UserProfile', on_delete=models.CASCADE)
    report_data = models.JSONField(verbose_name="周报数据")
    visualization_config = models.JSONField(verbose_name="可视化配置")
    generated_at = models.DateTimeField(auto_now_add=True)
    week_number = models.PositiveSmallIntegerField(verbose_name="周次")