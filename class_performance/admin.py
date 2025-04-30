from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, Homework, Exam, ClassInteraction, StudyBehavior

admin.site.register(Student)
admin.site.register(Homework)
admin.site.register(Exam)
admin.site.register(ClassInteraction)
admin.site.register(StudyBehavior)