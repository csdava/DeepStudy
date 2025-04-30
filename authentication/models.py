from django.db import models

# Create your models here.
class LoginHistory(models.Model):
    """
    用户登录历史记录
    """
    user = models.ForeignKey('user_management.UserProfile', on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    device_info = models.CharField(max_length=200)