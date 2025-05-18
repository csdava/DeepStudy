from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name="任务名称")
    description = models.TextField(verbose_name="任务描述")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tasks", verbose_name="创建者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title

class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="assignments", verbose_name="任务")
    assigned_to = models.ManyToManyField(User, related_name="assigned_tasks", verbose_name="分配对象")
    attachment = models.FileField(upload_to="attachments/", blank=True, null=True, verbose_name="附件")
    grading_criteria = models.TextField(verbose_name="评分标准")
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="权重")

    def __str__(self):
        return f"{self.task.title} - {self.assigned_to.all()}"

class TaskSubmission(models.Model):
    task_assignment = models.ForeignKey(TaskAssignment, on_delete=models.CASCADE, related_name="submissions", verbose_name="任务分配")
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions", verbose_name="提交者")
    submission_text = models.TextField(blank=True, null=True, verbose_name="文本提交内容")
    submission_file = models.FileField(upload_to="submissions/", blank=True, null=True, verbose_name="文件提交")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="提交时间")
    grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="评分")
    feedback = models.TextField(blank=True, null=True, verbose_name="反馈意见")

    def __str__(self):
        return f"{self.task_assignment.task.title} - {self.submitted_by.username}"