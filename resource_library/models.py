from django.db import models

# Create your models here.
class Resource(models.Model):
    """
    共享学习资源库
    """
    RESOURCE_TYPES = [
        ('PPT', '课件'),
        ('VIDEO', '视频'),
        ('DOC', '文档'),
        ('TEST', '试题')
    ]
    title = models.CharField(max_length=200, verbose_name="资源标题")
    uploader = models.ForeignKey('user_management.UserProfile', on_delete=models.CASCADE)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    file = models.FileField(upload_to='resources/%Y/%m/')
    description = models.TextField(blank=True, verbose_name="资源描述")
    related_class = models.ForeignKey('class_management.Class', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    download_count = models.PositiveIntegerField(default=0, verbose_name="下载次数")
    tags = models.JSONField(verbose_name="资源标签", default=list)