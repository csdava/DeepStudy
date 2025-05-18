# lesson_plan_generator/tasks.py
from celery import shared_task
from .models import LessonPlan
from .utils import generate_attachments

@shared_task
def generate_lesson_plan_task(plan_id):
    """
    异步生成教案相关文件
    """
    try:
        plan = LessonPlan.objects.get(id=plan_id)
        
        # 生成教案附件（Word和PPT）
        generate_attachments(plan)
        
        # 更新教案状态
        plan.status = 'completed'
        plan.save()
        
        return f"Successfully generated lesson plan and attachments for {plan.id}"
    except Exception as e:
        return f"Failed to generate lesson plan: {str(e)}"