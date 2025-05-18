# forms.py
from django import forms
from .models import DifficultyAnalysis


class DifficultyOptimizationForm(forms.Form):
    subject = forms.ChoiceField(
        label='学科',
        choices=DifficultyAnalysis.SUBJECT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        })
    )

    grade = forms.ChoiceField(
        label='年级',
        choices=DifficultyAnalysis.GRADE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        })
    )

    assignment_content = forms.CharField(
        label='作业内容',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'placeholder': '请输入完整的作业内容，包括：\n1. 题目\n2. 参考答案\n3. 解题思路（可选）',
            'required': True
        })
    )

    learning_objectives = forms.CharField(
        label='作业目标',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': '请描述本次作业的具体目标，例如：\n1. 巩固二次函数的基础知识\n2. 提升解应用题的能力\n3. 培养数学建模思维',
            'required': True
        })
    )

    average_score = forms.FloatField(
        label='班级平均分',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入最近一次考试的班级平均分（0-100）',
            'min': '0',
            'max': '100',
            'step': '0.1'
        }),
        required=False
    )

    score_distribution = forms.CharField(
        label='成绩分布',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': '请描述成绩分布情况，例如：\n优秀(90分以上): 20%\n良好(75-90分): 45%\n及格(60-75分): 25%\n不及格(60分以下): 10%'
        }),
        required=False
    )

    common_mistakes = forms.CharField(
        label='常见错误类型',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': '请列出学生在该知识点常见的错误类型，例如：\n1. 二次函数求解时经常忽略负根\n2. 应用题中数学建模能力不足'
        }),
        required=False
    )

    additional_notes = forms.CharField(
        label='补充说明',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': '其他需要说明的情况，如：\n1. 特殊学生情况\n2. 教学进度\n3. 特殊教学要求'
        }),
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        # 构建student_performance数据结构
        student_performance = {
            'average_score': cleaned_data.get('average_score'),
            'score_distribution': cleaned_data.get('score_distribution'),
            'common_mistakes': cleaned_data.get('common_mistakes'),
            'additional_notes': cleaned_data.get('additional_notes')
        }
        cleaned_data['student_performance'] = student_performance
        return cleaned_data