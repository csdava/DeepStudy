# models.py（扩展后的版本）
from django.db import models


class GeneratedTest(models.Model):
    """
    AI生成测试题记录（增强版）
    """
    QUESTION_TYPES = (
        ('single_choice', '单选题'),
        ('multiple_choice', '多选题'),
        ('fill_in_blank', '填空题'),
        ('short_answer', '简答题'),
        ('essay', '论述题'),
    )

    DIFFICULTY_LEVELS = (
        ('basic', '基础'),
        ('intermediate', '中等'),
        ('advanced', '困难'),
    )

    student = models.ForeignKey('user_management.UserProfile', on_delete=models.CASCADE)
    knowledge_point = models.CharField(max_length=200, verbose_name="知识点")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, verbose_name="题型")
    quantity = models.PositiveIntegerField(verbose_name="题目数量", default=5)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, verbose_name="难度等级")
    generated_content = models.JSONField(verbose_name="生成内容", help_text="包含题目、选项、答案的结构化数据")
    validation_status = models.BooleanField(verbose_name="校验状态", default=False)
    test_link = models.CharField(max_length=100, verbose_name="测试入口", blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "生成测试"
        verbose_name_plural = "生成测试管理"

    def __str__(self):
        return f"{self.student}的{self.knowledge_point}测试题"