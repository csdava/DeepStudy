# forms.py
from django import forms
from .models import LessonPlan

class LessonPlanForm(forms.ModelForm):
    MATERIAL_CHOICES = [
        ('ppt', 'PPT提纲'),
        ('quiz', '互动题目'),
        ('homework', '作业建议'),
    ]

    materials = forms.MultipleChoiceField(
        label='课件需求',
        choices=MATERIAL_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text='选择需要生成的课件类型'
    )

    class Meta:
        model = LessonPlan
        fields = [
            'subject', 'grade', 'duration', 'objectives',
            'key_points', 'difficulties', 'materials',
            'teaching_style', 'student_profile'
        ]
        labels = {
            'subject': '学科',
            'grade': '年级',
            'duration': '课时',
            'objectives': '教学目标',
            'key_points': '重点内容',
            'difficulties': '教学难点',
            'teaching_style': '教学方式',
            'student_profile': '学生情况'
        }
        help_texts = {
            'objectives': '描述本节课要达到的教学目标',
            'key_points': '列出本节课的重点知识点，用逗号分隔',
            'difficulties': '描述本节课的教学难点和重点关注内容',
            'student_profile': '描述学生的整体情况，如：知识基础、学习能力等'
        }
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'grade': forms.Select(attrs={'class': 'form-select'}),
            'duration': forms.Select(
                attrs={'class': 'form-select'},
                choices=[
                    ('40', '40分钟'),
                    ('80', '双课时（80分钟）')
                ]
            ),
            'teaching_style': forms.Select(attrs={'class': 'form-select'}),
            'key_points': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '用逗号分隔多个知识点'
            }),
            'objectives': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '请输入本节课的教学目标',
                'rows': 3
            }),
            'difficulties': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '请输入本节课的教学难点',
                'rows': 3
            }),
            'student_profile': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '请描述学生的整体情况，如：知识基础、学习能力等',
                'rows': 3
            })
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.materials_needed = {
            item: (item in self.cleaned_data['materials'])
            for item in dict(self.MATERIAL_CHOICES)
        }
        if commit:
            instance.save()
        return instance