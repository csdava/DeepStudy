from django.contrib import admin
from .models import Task, TaskAssignment, TaskSubmission

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_by', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_by',)

@admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
    def get_assigned_users(self, obj):
        return ", ".join([user.username for user in obj.assigned_to.all()])
    get_assigned_users.short_description = "分配对象"
    
    list_display = ('task', 'get_assigned_users', 'attachment', 'grading_criteria', 'weight')
    search_fields = ('task__title',)
    filter_horizontal = ('assigned_to',)

@admin.register(TaskSubmission)
class TaskSubmissionAdmin(admin.ModelAdmin):
    list_display = ('task_assignment', 'submitted_by', 'submitted_at', 'grade')
    search_fields = ('task_assignment__task__title', 'submitted_by__username')