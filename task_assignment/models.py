from django.db import models
from class_management.models import Class

class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name='任务标题')
    description = models.TextField(verbose_name='任务描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    class_info = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='tasks', verbose_name='所属班级')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '任务'
        verbose_name_plural = '任务'

    def __str__(self):
        return self.title
