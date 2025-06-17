from django.db import models
from class_management.models import Class, Student

class Exam(models.Model):
    name = models.CharField(max_length=100, verbose_name='考试名称', default='未命名考试')
    exam_date = models.DateField(verbose_name='考试日期')
    class_info = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='exams', verbose_name='班级', default=1)

    def __str__(self):
        return f"{self.class_info.name} - {self.name}"

    class Meta:
        verbose_name = '考试'
        verbose_name_plural = '考试'

class Score(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='scores', verbose_name='考试')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='scores', verbose_name='学生')
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='分数')

    def __str__(self):
        return f"{self.student.name} - {self.exam.name} - {self.score}"

    class Meta:
        verbose_name = '成绩'
        verbose_name_plural = '成绩'
