from django.db import models
from django.utils import timezone

class Student(models.Model):
    name = models.CharField(max_length=100, verbose_name='姓名')
    student_id = models.CharField(max_length=20, unique=True, verbose_name='学号')
    class_name = models.CharField(max_length=50, default='未分配', verbose_name='班级')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = '学生'

    def __str__(self):
        return f"{self.name} ({self.student_id})"

class Homework(models.Model):
    title = models.CharField(max_length=200, verbose_name='作业标题')
    description = models.TextField(verbose_name='作业描述')
    due_date = models.DateTimeField(verbose_name='截止日期')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='学生')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='分数')
    submitted = models.BooleanField(default=False, verbose_name='是否已提交')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '作业'
        verbose_name_plural = '作业'

    def __str__(self):
        return f"{self.title} - {self.student.name}"

class Exam(models.Model):
    title = models.CharField(max_length=200, verbose_name='考试标题')
    exam_date = models.DateTimeField(verbose_name='考试日期')
    duration = models.IntegerField(verbose_name='考试时长(分钟)')
    total_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='总分')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='学生')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='得分')
    exam_type = models.CharField(max_length=50, choices=[
        ('midterm', '期中考试'),
        ('final', '期末考试'),
        ('quiz', '小测验'),
        ('other', '其他')
    ], verbose_name='考试类型')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '考试'
        verbose_name_plural = '考试'

    def __str__(self):
        return f"{self.title} - {self.student.name}"

class LearningBehavior(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='学生')
    date = models.DateField(verbose_name='日期')
    attendance = models.BooleanField(default=True, verbose_name='出勤情况')
    participation_score = models.IntegerField(
        choices=[(i, i) for i in range(6)],  # 0-5分
        verbose_name='课堂参与度'
    )
    homework_completion = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        verbose_name='作业完成率',
        help_text='百分比形式，例如：85.5表示85.5%'
    )
    study_time = models.IntegerField(
        verbose_name='学习时长(分钟)',
        help_text='每天的学习时长'
    )
    notes = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='备注'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '学习行为'
        verbose_name_plural = '学习行为'
        unique_together = ['student', 'date']  # 确保每个学生每天只有一条记录

    def __str__(self):
        return f"{self.student.name} - {self.date}"
