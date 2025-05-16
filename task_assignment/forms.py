from django import forms
from .models import Task, Assignment, Submission

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['assigned_to', 'due_date']

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['content']