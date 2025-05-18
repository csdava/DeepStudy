# models.py（扩展版）
from django.db import models


class DifficultyAnalysis(models.Model):
    GRADE_CHOICES = [
        ('P3', '小学三年级'),
        ('P4', '小学四年级'),
        ('P5', '小学五年级'),
        ('P6', '小学六年级'),
        ('J1', '初中一年级'),
        ('J2', '初中二年级'),
        ('J3', '初中三年级'),
        ('H1', '高中一年级'),
        ('H2', '高中二年级'),
        ('H3', '高中三年级'),
    ]

    SUBJECT_CHOICES = [
        ('math', '数学'),
        ('chinese', '语文'),
        ('english', '英语'),
        ('physics', '物理'),
        ('chemistry', '化学'),
        ('biology', '生物'),
        ('history', '历史'),
        ('geography', '地理'),
        ('politics', '政治'),
    ]

    DIFFICULTY_LEVELS = [
        ('too_easy', '过于简单'),
        ('easy', '偏简单'),
        ('appropriate', '适中'),
        ('hard', '偏难'),
        ('too_hard', '过于困难'),
    ]

    # 基本信息
    assignment_id = models.UUIDField(verbose_name="作业ID", unique=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, verbose_name="学科")
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES, verbose_name="年级")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 输入参数
    assignment_content = models.TextField(verbose_name="作业内容")
    learning_objectives = models.TextField(verbose_name="学习目标")
    student_performance = models.JSONField(verbose_name="学生学情数据")
    
    # 分析结果
    difficulty_level = models.CharField(
        max_length=20, 
        choices=DIFFICULTY_LEVELS, 
        verbose_name="难度评级"
    )
    knowledge_coverage = models.JSONField(
        verbose_name="知识点覆盖",
        help_text="包含知识点列表及其难度评估"
    )
    thinking_levels = models.JSONField(
        verbose_name="思维层次",
        help_text="布鲁姆分类法各层次占比"
    )
    
    # 优化建议
    difficulty_adjustment = models.JSONField(
        verbose_name="难度调整建议",
        help_text="具体的难度调整建议"
    )
    question_type_suggestions = models.JSONField(
        verbose_name="题型建议",
        help_text="建议增加或调整的题型"
    )
    sequence_optimization = models.JSONField(
        verbose_name="顺序优化",
        help_text="题目顺序调整建议"
    )
    personalized_suggestions = models.JSONField(
        verbose_name="个性化建议",
        help_text="针对不同水平学生的建议"
    )
    
    # 可视化数据
    visualization_data = models.JSONField(
        verbose_name="可视化数据",
        help_text="用于前端展示的图表数据"
    )
    
    # 反馈
    teacher_feedback = models.FloatField(
        verbose_name="教师反馈评分",
        null=True,
        help_text="教师对分析结果的评分(1-5分)"
    )
    feedback_comments = models.TextField(
        verbose_name="反馈意见",
        blank=True,
        help_text="教师的具体反馈意见"
    )

    class Meta:
        verbose_name = "作业难度分析"
        verbose_name_plural = "作业难度分析记录"

    def __str__(self):
        return f"{self.get_subject_display()} {self.get_grade_display()} 作业分析"