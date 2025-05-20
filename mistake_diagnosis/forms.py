from django import forms

class MistakeDiagnosisForm(forms.Form):
    SUBJECT_CHOICES = [
        ('math', '数学'),
        ('chinese', '语文'),
        ('english', '英语'),
        ('physics', '物理'),
        ('chemistry', '化学'),
        ('biology', '生物'),
        ('history', '历史'),
        ('geography', '地理'),
        ('politics', '政治'),
    ]

    subject = forms.ChoiceField(
        label='学科',
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    knowledge_point = forms.CharField(
        label='知识点',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入具体知识点，如：数学-函数、语文-文言文等'
        })
    )

    question_text = forms.CharField(
        label='题目内容',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': '请输入完整的题目内容'
        })
    )

    student_answer = forms.CharField(
        label='你的答案',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': '请输入你的答案'
        })
    )

    self_analysis = forms.CharField(
        label='自我分析（可选）',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': '你认为错在哪里？有什么想法？'
        })
    ) 