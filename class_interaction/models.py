from django.db import models

# Create your models here.
class DiscussionThread(models.Model):
    """
    班级讨论主题
    """
    class_instance = models.ForeignKey('class_management.Class', on_delete=models.CASCADE)
    creator = models.ForeignKey('user_management.UserProfile', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_pinned = models.BooleanField(default=False)

class DiscussionReply(models.Model):
    """
    讨论回复记录
    """
    thread = models.ForeignKey(DiscussionThread, on_delete=models.CASCADE)
    author = models.ForeignKey('user_management.UserProfile', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)