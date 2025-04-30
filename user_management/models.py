
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# 如果需要使用 JSONField，确保已安装 django-jsonfield 并从相应位置导入
# from jsonfield import JSONField

ROLE_CHOICES = [
    ('STU', '学生'),
    ('TCH', '教师'),
    ('ADM', '管理员')
]

class UserProfile(AbstractUser):
    """
    系统用户核心模型（支持多角色）
    """
    role = models.CharField(max_length=3, choices=ROLE_CHOICES, verbose_name="用户角色")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="头像")
    school = models.CharField(max_length=100, verbose_name="所属学校", default='未设置')
    grade = models.CharField(max_length=20, verbose_name="年级", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最后更新时间")
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    class Meta:
        verbose_name = "用户档案"
        verbose_name_plural = verbose_name

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="userprofile_groups",  # 唯一名称
        related_query_name="userprofile",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="userprofile_permissions",  # 唯一名称
        related_query_name="userprofile",
    )

    # 注意：groups 和 user_permissions 已经由 AbstractUser 提供，无需重新定义

class TeacherProfile(models.Model):
    """
    教师扩展信息
    """
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='teacher_profile')
    subject = models.CharField(max_length=50, verbose_name="教学科目")
    teaching_years = models.IntegerField(default=0, verbose_name="教龄")
    expert_level = models.CharField(max_length=20, verbose_name="教学等级", default='初级')

class StudentProfile(models.Model):
    """
    学生扩展信息
    """
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='student_profile')
    parent_contact = models.CharField(max_length=100, verbose_name="家长联系方式", blank=True)
    # 使用 TextField 存储 JSON 数据
    learning_style = models.TextField(verbose_name="学习风格分析结果", default=dict)  # 注意：这里 default=dict 不会按预期工作，应为 JSON 字符串
    knowledge_map = models.TextField(verbose_name="知识掌握图谱", default=dict)