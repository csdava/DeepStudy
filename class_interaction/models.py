from django.db import models
from django.contrib.auth.models import User

class DiscussionTopic(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    scope = models.CharField(max_length=50)  # 班级、小组等
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class DiscussionPost(models.Model):
    topic = models.ForeignKey(DiscussionTopic, on_delete=models.CASCADE)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    is_pinned = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"Post by {self.created_by} on {self.topic}"

class InteractionStatistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Stats for {self.user}"