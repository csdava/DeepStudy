# lesson_plan_generator/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import LessonPlan  # 添加模型导入

@receiver(pre_save, sender=LessonPlan)
def update_version(_sender, instance, **kwargs):  # 使用下划线忽略未用参数
    if instance.pk:
        original = LessonPlan.objects.get(pk=instance.pk)
        if original.generated_content != instance.generated_content:
            instance.version = f"{float(original.version)+0.1:.1f}"
            instance.previous_version = original