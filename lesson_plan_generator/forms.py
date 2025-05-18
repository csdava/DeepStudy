# forms.py
from django import forms
from .models import LessonPlan

class LessonPlanForm(forms.ModelForm):
    MATERIAL_CHOICES = [
        ('ppt', 'PPT提纲'),
        ('quiz', '互动题目'),
        ('homework', '作业建议'),
    ]

    DURATION_CHOICES = [
        ('40分钟', '40分钟'),
        ('45分钟', '45分钟'),
        ('50分钟', '50分钟'),
        ('80分钟', '80分钟（双课时）'),
        ('1课时', '1课时'),
        ('1.5课时', '1.5课时'),
        ('2课时', '2课时'),
        ('3课时', '3课时'),
        ('4课时', '4课时'),
        ('custom', '自定义'),
    ]

    materials = forms.MultipleChoiceField(
        label='课件需求',
        choices=MATERIAL_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text='选择需要生成的课件类型'
    )

    duration = forms.ChoiceField(
        label='课时',
        choices=DURATION_CHOICES,
        initial='45分钟',
        widget=forms.Select(attrs={'class': 'form-select duration-select'}),
        help_text='选择预设课时或选择"自定义"输入其他时长'
    )

    custom_duration = forms.CharField(
        label='自定义课时',
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control custom-duration',
            'placeholder': '例如：60分钟、2.5课时等',
            'style': 'display: none;'
        })
    )

    class Meta:
        model = LessonPlan
        fields = [
            'subject', 'grade', 'duration',
            'objectives', 'key_points', 'difficulties',
            'materials', 'teaching_style', 'student_profile'
        ]
        labels = {
            'subject': '学科',
            'grade': '年级',
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

    def clean(self):
        cleaned_data = super().clean()
        duration_choice = cleaned_data.get('duration')
        custom_duration = cleaned_data.get('custom_duration')

        if duration_choice == 'custom' and not custom_duration:
            raise forms.ValidationError({
                'custom_duration': '选择自定义课时时，必须填写具体时长'
            })

        if duration_choice == 'custom':
            cleaned_data['duration'] = custom_duration

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        # 保存课时
        if self.cleaned_data.get('duration') == 'custom':
            instance.duration = self.cleaned_data.get('custom_duration')
        else:
            instance.duration = self.cleaned_data.get('duration')
            
        # 保存材料需求
        instance.materials_needed = {
            item: (item in self.cleaned_data['materials'])
            for item in dict(self.MATERIAL_CHOICES)
        }
        
        if commit:
            instance.save()
        return instance

    class Media:
        js = ('js/lesson_plan_form.js',)