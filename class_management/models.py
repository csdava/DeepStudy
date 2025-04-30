from django.db import models
from user_management.models import UserProfile
# Create your models here.
class Class(models.Model):
    """
    班级核心信息模型
    """
    name = models.CharField(max_length=100, verbose_name="班级名称")
    code = models.CharField(max_length=20, unique=True, verbose_name="班级代码")
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='managed_classes')
    students = models.ManyToManyField(UserProfile, related_name='enrolled_classes', blank=True)
    start_date = models.DateField(verbose_name="开班日期")
    schedule = models.JSONField(verbose_name="课程安排表")
    subject = models.CharField(max_length=50, verbose_name="所属学科")

    class Meta:
        verbose_name = "班级管理"
        ordering = ['-start_date']

class SubjectCurriculum(models.Model):
    """
    学科课程大纲
    """
    subject = models.CharField(max_length=50, verbose_name="学科名称")
    grade_level = models.CharField(max_length=20, verbose_name="适用学段")
    content = models.JSONField(verbose_name="课程大纲结构")
    version = models.CharField(max_length=20, verbose_name="版本号")