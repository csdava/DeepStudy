from django.contrib import admin
from .models import Exam, Score

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_date', 'class_info')
    list_filter = ('class_info', 'exam_date')
    search_fields = ('name', 'class_info__name')

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'score')
    list_filter = ('exam__class_info', 'exam')
    search_fields = ('student__name', 'exam__name')
