# forms.py
from django import forms

class MistakeDiagnosisForm(forms.Form):
    SUBJECT_CHOICES = [
        ('math', '数学'),
        ('chinese', '语文'),
        ('english', '英语'),
        # 其他学科...
    ]

    subject = forms.ChoiceField(
        label='学科',
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    knowledge_point = forms.CharField(
        label='知识点',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    question_text = forms.CharField(
        label='题目内容',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    student_answer = forms.CharField(
        label='你的答案',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    self_analysis = forms.CharField(
        label='自我分析（可选）',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )