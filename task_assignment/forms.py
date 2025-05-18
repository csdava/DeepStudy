from django import forms
from .models import Task, TaskAssignment, TaskSubmission
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']
        labels = {
            'title': '任务名称',
            'description': '任务描述'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4})
        }

class TaskAssignmentForm(forms.ModelForm):
    class Meta:
        model = TaskAssignment
        fields = ['assigned_to', 'attachment', 'grading_criteria', 'weight']
        labels = {
            'assigned_to': '分配给',
            'attachment': '附件',
            'grading_criteria': '评分标准',
            'weight': '权重'
        }
        widgets = {
            'grading_criteria': forms.Textarea(attrs={'rows': 3}),
            'weight': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100'})
        }

class TaskSubmissionForm(forms.ModelForm):
    class Meta:
        model = TaskSubmission
        fields = ['submission_text', 'submission_file']
        labels = {
            'submission_text': '提交内容',
            'submission_file': '提交文件'
        }
        widgets = {
            'submission_text': forms.Textarea(attrs={'rows': 4})
        }