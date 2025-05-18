# lesson_plan_generator/views.py
# 添加缺失的导入
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
import logging
from docx import Document  # 需要先安装python-docx
from pptx import Presentation  # 需要先安装python-pptx
import uuid  # 保留以用于可能需要的UUID生成
from .models import LessonPlan
from .forms import LessonPlanForm
from .tasks import generate_lesson_plan_task
from .utils import generate_attachments
from .ai_generator import LessonPlanAIGenerator
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY', 'sk-bc14211e98e3444e96b04c818666e128'),  # 从环境变量获取
    base_url="https://api.deepseek.com"
)

logger = logging.getLogger(__name__)

def lesson_plan_list(request):
    """显示所有教案列表"""
    lesson_plans = LessonPlan.objects.all().order_by('-created_at')
    return render(request, 'lesson_plan_generator/lesson_list.html', {'lesson_plans': lesson_plans})

def generate_lesson_plan(request):
    if request.method == 'POST':
        form = LessonPlanForm(request.POST)
        if form.is_valid():
            lesson_plan = form.save(commit=False)
            
            try:
                # 使用AI生成教案内容
                logger.info("开始调用AI生成教案...")
                ai_generator = LessonPlanAIGenerator()
                logger.info(f"输入参数: subject={lesson_plan.get_subject_display()}, grade={lesson_plan.get_grade_display()}")
                
                ai_content = ai_generator.generate_lesson_plan(
                    subject=lesson_plan.get_subject_display(),
                    grade=lesson_plan.get_grade_display(),
                    objectives=lesson_plan.objectives,
                    duration=str(lesson_plan.duration),
                    key_points=lesson_plan.key_points.split(',') if lesson_plan.key_points else None,
                    difficulties=lesson_plan.difficulties,
                    teaching_style=lesson_plan.get_teaching_style_display(),
                    student_profile=lesson_plan.student_profile
                )
                
                logger.info("AI返回内容：%s", ai_content)
                
                # 更新教案内容
                lesson_plan.objectives = ai_content['sections']['objectives']
                lesson_plan.key_points = ai_content['sections']['steps']
                lesson_plan.difficulties = ai_content['sections']['strategies']
                lesson_plan.generated_content = ai_content['content']
                
                logger.info("更新后的教案内容：")
                logger.info(f"objectives: {lesson_plan.objectives}")
                logger.info(f"key_points: {lesson_plan.key_points}")
                logger.info(f"difficulties: {lesson_plan.difficulties}")
                logger.info(f"generated_content: {lesson_plan.generated_content}")
                
                lesson_plan.save()
                
                # 生成附件
                generate_attachments(lesson_plan, ai_content)
                messages.success(request, '教案生成成功！')
                
            except Exception as e:
                logger.error(f"AI生成教案失败：{str(e)}", exc_info=True)
                messages.error(request, '生成教案时出错，请稍后重试。')
                return render(request, 'lesson_plan_generator/create_lesson.html', {'form': form})
            
            return redirect('lesson_detail', pk=lesson_plan.id)
    else:
        form = LessonPlanForm()
    
    return render(request, 'lesson_plan_generator/create_lesson.html', {'form': form})

def lesson_plan_detail(request, pk):
    lesson_plan = get_object_or_404(LessonPlan, pk=pk)
    
    # 检查文件是否存在
    from .utils import get_file_path
    import os
    
    docx_path = get_file_path(lesson_plan.id, 'docx')
    pptx_path = get_file_path(lesson_plan.id, 'pptx')
    
    context = {
        'lesson': lesson_plan,
        'docx_exists': os.path.exists(docx_path),
        'pptx_exists': os.path.exists(pptx_path)
    }
    
    return render(request, 'lesson_plan_generator/lesson_detail.html', context)

def edit_lesson_plan(request, pk):
    lesson_plan = get_object_or_404(LessonPlan, pk=pk)
    if request.method == 'POST':
        form = LessonPlanForm(request.POST, instance=lesson_plan)
        if form.is_valid():
            lesson_plan = form.save()
            
            try:
                # 重新生成教案附件
                generate_attachments(lesson_plan)
                messages.success(request, '教案更新成功！')
            except Exception as e:
                logger.error(f"更新教案附件时出错：{str(e)}", exc_info=True)
                messages.error(request, '教案已保存，但更新附件时出错。请稍后重试。')
            
            return redirect('lesson_detail', pk=pk)
    else:
        form = LessonPlanForm(instance=lesson_plan)
    
    return render(request, 'lesson_plan_generator/edit_lesson.html', {'form': form, 'lesson': lesson_plan})

def share_lesson(request, pk):
    lesson_plan = get_object_or_404(LessonPlan, pk=pk)
    # 实现分享逻辑
    return render(request, 'lesson_plan_generator/share_lesson.html', {'lesson': lesson_plan})