from django.db import models

# Create your models here.
class LessonPlan(models.Model):
    """
    AI生成教案存储
    """
    teacher = models.ForeignKey('user_management.UserProfile', on_delete=models.CASCADE)
    input_parameters = models.JSONField(verbose_name="生成参数")
    generated_content = models.JSONField(verbose_name="教案内容")
    version = models.CharField(max_length=20, verbose_name="版本号")
    created_at = models.DateTimeField(auto_now_add=True)
    is_template = models.BooleanField(default=False, verbose_name="是否作为模板")