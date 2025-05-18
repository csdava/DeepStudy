from django.db import models
from django.utils import timezone
import datetime

class LearningRecord(models.Model):
    date = models.DateField()
    study_duration = models.PositiveIntegerField(help_text="学习时长（分钟）")
    resource_usage = models.JSONField(default=dict)  # 资源使用情况
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'learning_report_learningrecord'
        verbose_name = "学习记录"
        verbose_name_plural = "学习记录"

class AssignmentRecord(models.Model):
    week = models.CharField(max_length=8)  # 格式: YYYYWW
    submission_rate = models.FloatField()  # 作业提交率
    accuracy_rate = models.FloatField()   # 正确率
    subject = models.CharField(max_length=20)  # 学科
    assignment_details = models.JSONField(default=dict)  # 作业详细信息
    submission_date = models.DateTimeField(default=timezone.now)  # 记录创建时间

    class Meta:
        db_table = 'learning_report_assignmentrecord'
        verbose_name = "作业记录"
        verbose_name_plural = "作业记录"

class TestRecord(models.Model):
    week = models.CharField(max_length=8)  # 格式: YYYYWW
    subject = models.CharField(max_length=20)  # 学科
    score = models.FloatField()
    wrong_questions = models.JSONField(default=list)  # 错题ID列表
    knowledge_points = models.JSONField(default=dict)  # 知识点掌握情况

    class Meta:
        db_table = 'learning_report_testrecord'
        verbose_name = "测试记录"
        verbose_name_plural = "测试记录"

class InteractionRecord(models.Model):
    date = models.DateField()
    interaction_type = models.CharField(max_length=20, choices=[
        ('question', '提问'),
        ('answer', '回答'),
        ('discussion', '讨论'),
        ('group_work', '小组活动'),
    ])
    content = models.TextField()  # 互动内容
    subject = models.CharField(max_length=20)  # 学科

    class Meta:
        db_table = 'learning_report_interactionrecord'
        verbose_name = "互动记录"
        verbose_name_plural = "互动记录"

class WeeklyReport(models.Model):
    week = models.CharField(max_length=8)  # 格式: YYYYWW
    start_date = models.DateField()
    end_date = models.DateField()
    
    # 统计数据
    total_study_time = models.PositiveIntegerField(default=0)  # 总学习时长（分钟）
    avg_submission_rate = models.FloatField(default=0)  # 平均作业提交率
    avg_accuracy_rate = models.FloatField(default=0)  # 平均正确率
    avg_test_score = models.FloatField(default=0)  # 平均测试分数
    interaction_count = models.PositiveIntegerField(default=0)  # 互动次数
    
    # 详细数据
    subject_performance = models.JSONField(default=dict)  # 各科目表现
    knowledge_mastery = models.JSONField(default=dict)  # 知识点掌握情况
    resource_usage_stats = models.JSONField(default=dict)  # 资源使用统计
    
    # AI生成内容
    performance_analysis = models.TextField(blank=True)  # AI生成的表现分析
    improvement_suggestions = models.TextField(blank=True)  # 改进建议
    next_week_plan = models.TextField(blank=True)  # 下周计划建议
    
    # 可视化数据
    visualization_data = models.JSONField(default=dict)  # 存储图表所需的数据
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'learning_report_weeklyreport'
        verbose_name = "周报"
        verbose_name_plural = "周报"
        unique_together = ['week']
        app_label = 'learning_report'

    @classmethod
    def get_week_range(cls, date=None):
        """获取指定日期所在的周的起止日期"""
        if date is None:
            date = timezone.now().date()
        start_date = date - datetime.timedelta(days=date.weekday())
        end_date = start_date + datetime.timedelta(days=6)
        return start_date, end_date

    def generate_report(self):
        """生成周报内容"""
        # 这个方法将在views中实现具体的报告生成逻辑
        pass