from django.db import models
from user_management.models import UserProfile
# Create your models here.
class Assignment(models.Model):
    """
    作业任务核心模型
    """
    STATUS_CHOICES = [
        ('DRAFT', '草稿'),
        ('PUBLISHED', '已发布'),
        ('CLOSED', '已关闭')
    ]
    title = models.CharField(max_length=200, verbose_name="作业标题")
    content = models.TextField(verbose_name="作业内容")
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_assignments')
    target_class = models.ForeignKey('class_management.Class', on_delete=models.CASCADE)
    deadline = models.DateTimeField(verbose_name="截止时间")
    difficulty = models.FloatField(verbose_name="初始难度系数", default=1.0)
    attachments = models.ManyToManyField('resource_library.Resource', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    ai_analysis = models.JSONField(verbose_name="AI难度分析结果", default=dict)

class Submission(models.Model):
    """
    学生作业提交记录
    """
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='submissions')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    content = models.TextField(verbose_name="提交内容")
    score = models.FloatField(null=True, blank=True, verbose_name="得分")
    feedback = models.TextField(blank=True, verbose_name="教师反馈")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="提交时间")
    ai_review = models.JSONField(verbose_name="AI批改分析结果", default=dict)