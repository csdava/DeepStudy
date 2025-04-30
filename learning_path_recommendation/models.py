from django.db import models

# Create your models here.
class LearningPath(models.Model):
    """
    个性化学习路径推荐
    """
    student = models.ForeignKey('user_management.UserProfile', on_delete=models.CASCADE)
    recommended_path = models.JSONField(verbose_name="推荐路径")
    generated_at = models.DateTimeField(auto_now_add=True)
    effectiveness = models.FloatField(verbose_name="路径有效性评分", null=True)
    adjustment_history = models.JSONField(verbose_name="调整记录", default=list)