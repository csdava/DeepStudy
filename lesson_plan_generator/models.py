# models.py（扩展版）
from django.db import models


class LessonPlan(models.Model):
    SUBJECT_CHOICES = [
        # 语文
        ('chinese', '语文'),
        # 数学
        ('math', '数学'),
        # 英语
        ('english', '英语'),
        # 物理
        ('physics', '物理'),
        # 化学
        ('chemistry', '化学'),
        # 生物
        ('biology', '生物'),
        # 政治
        ('politics', '政治'),
        # 历史
        ('history', '历史'),
        # 地理
        ('geography', '地理'),
        # 其他外语
        ('japanese', '日语'),
        ('korean', '韩语'),
        ('french', '法语'),
        ('german', '德语'),
        ('russian', '俄语'),
        # 信息技术
        ('it', '信息技术'),
        # 音乐
        ('music', '音乐'),
        # 美术
        ('art', '美术'),
        # 体育
        ('pe', '体育'),
    ]

    GRADE_CHOICES = [
        # 小学
        ('P1', '小学一年级'),
        ('P2', '小学二年级'),
        ('P3', '小学三年级'),
        ('P4', '小学四年级'),
        ('P5', '小学五年级'),
        ('P6', '小学六年级'),
        # 初中
        ('J1', '初中一年级'),
        ('J2', '初中二年级'),
        ('J3', '初中三年级'),
        # 高中
        ('H1', '高中一年级'),
        ('H2', '高中二年级'),
        ('H3', '高中三年级'),
        # 大学
        ('U1', '大学一年级'),
        ('U2', '大学二年级'),
        ('U3', '大学三年级'),
        ('U4', '大学四年级'),
        # 研究生
        ('G1', '研究生一年级'),
        ('G2', '研究生二年级'),
        ('G3', '研究生三年级'),
    ]

    TEACHING_STYLE_CHOICES = [
        ('inspire', '启发式'),
        ('inquiry', '探究式'),
        ('lecture', '讲授式'),
        ('discussion', '讨论式'),
        ('practice', '实践式'),
        ('group', '小组合作式'),
        ('game', '游戏教学式'),
        ('project', '项目式'),
        ('case', '案例式'),
        ('mixed', '混合式'),
    ]

    teacher = models.ForeignKey('user_management.UserProfile', on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='chinese', verbose_name='学科')
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES, default='P1', verbose_name='年级')
    duration = models.CharField(max_length=50, default='45分钟', verbose_name='课时', help_text='例如：45分钟、2课时、1.5课时等')
    objectives = models.TextField(default='', verbose_name='教学目标')
    key_points = models.TextField(blank=True, default='', verbose_name='重点内容')
    difficulties = models.TextField(blank=True, default='', verbose_name='教学难点')
    materials_needed = models.TextField(default='{}', verbose_name='教学材料')
    teaching_style = models.CharField(max_length=20, choices=TEACHING_STYLE_CHOICES, default='lecture', blank=True, verbose_name='教学方式')
    student_profile = models.TextField(blank=True, default='', verbose_name='学生情况')
    generated_content = models.TextField(default='{}', verbose_name='AI生成内容')
    version = models.CharField(max_length=20, default='1.0', verbose_name='版本号')
    previous_version = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_template = models.BooleanField(default=False, verbose_name='是否为模板')
    shared_classes = models.ManyToManyField('class_management.Class', blank=True, verbose_name='共享班级')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '教案'
        verbose_name_plural = '教案'

    def __str__(self):
        return f"{self.get_subject_display()}-{self.get_grade_display()}-v{self.version}"