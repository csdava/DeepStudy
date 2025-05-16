from django import forms
import re


class StudentInfoForm(forms.Form):
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

    PROGRESS_CHOICES = [
        ('beginner', '入门阶段 (0-30%)'),
        ('intermediate', '进行中 (30-60%)'),
        ('advanced', '深入阶段 (60-90%)'),
        ('expert', '巩固提高 (90-100%)'),
    ]

    LEARNING_STYLE_CHOICES = [
        ('visual', '视觉学习 (偏好图表、视频)'),
        ('auditory', '听觉学习 (偏好讲解、音频)'),
        ('reading', '阅读学习 (偏好文字材料)'),
        ('kinesthetic', '实践学习 (偏好动手操作)'),
    ]

    GOAL_CHOICES = [
        ('exam_prep', '备考提分'),
        ('knowledge', '知识扩展'),
        ('skill', '技能提升'),
        ('interest', '兴趣发展'),
    ]

    subject = forms.ChoiceField(
        label='学科选择',
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    current_progress = forms.ChoiceField(
        label='当前学习进度',
        choices=PROGRESS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    progress_detail = forms.CharField(
        label='进度详细说明',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': '请详细描述已掌握的知识点和待提高的部分...'
        }),
        required=False
    )

    learning_goal = forms.MultipleChoiceField(
        label='学习目标',
        choices=GOAL_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    goal_detail = forms.CharField(
        label='目标详细说明',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': '请具体描述您想达到的学习目标...'
        })
    )

    learning_style = forms.ChoiceField(
        label='学习方式偏好',
        choices=LEARNING_STYLE_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )

    learning_time = forms.IntegerField(
        label='每日可投入学习时间(分钟)',
        min_value=15,
        max_value=480,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入15-480之间的数值'
        })
    )

    recent_scores = forms.CharField(
        label='近期考试成绩',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': '请输入近三次考试成绩，例如：85,92,88'
        }),
        required=False
    )

    historical_data = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )