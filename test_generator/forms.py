# test_generator/forms.py
from django import forms

class TestGenerationForm(forms.Form):
    knowledge_point = forms.CharField(
        label='知识点',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入具体知识点，如：数学-函数、语文-文言文等'
        }),
        help_text='请尽可能具体地描述知识点，包括学科和具体内容'
    )

    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', '选择题'),
        ('fill_blank', '填空题'),
        ('short_answer', '简答题'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', '简单'),
        ('medium', '中等'),
        ('hard', '困难'),
    ]

    QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]

    question_type = forms.ChoiceField(
        label='题型',
        choices=QUESTION_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    quantity = forms.ChoiceField(
        label='题目数量',
        choices=QUANTITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    difficulty = forms.ChoiceField(
        label='难度',
        choices=DIFFICULTY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )