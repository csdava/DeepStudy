# models.py（扩展版）
from django.db import models


class LessonPlan(models.Model):
    SUBJECT_CHOICES = [
        ('math', '数学'),
        ('chinese', '语文'),
        ('english', '英语'),
        ('physics', '物理'),
    ]

    GRADE_CHOICES = [
        ('P5', '小学五年级'),
        ('J2', '初中二年级'),
        ('H1', '高中一年级'),
    ]

    TEACHING_STYLE_CHOICES = [
        ('inspire', '启发式'),
        ('inquiry', '探究式'),
        ('lecture', '讲授式'),
    ]

    teacher = models.ForeignKey('user_management.UserProfile', on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='math')
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES, default='P5')
    duration = models.CharField(max_length=20, default='45分钟')
    objectives = models.TextField(default='')
    key_points = models.TextField(blank=True, default='')  # 存储为逗号分隔的字符串
    difficulties = models.TextField(blank=True, default='')
    materials_needed = models.TextField(default='{}')  # 存储为JSON字符串
    teaching_style = models.CharField(max_length=20, choices=TEACHING_STYLE_CHOICES, default='lecture', blank=True)
    student_profile = models.TextField(blank=True, default='')
    generated_content = models.TextField(default='{}')  # 存储为JSON字符串
    version = models.CharField(max_length=20, default='1.0')
    previous_version = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_template = models.BooleanField(default=False)
    shared_classes = models.ManyToManyField('class_management.Class', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_subject_display()}教案-v{self.version}"