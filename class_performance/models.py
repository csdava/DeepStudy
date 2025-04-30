from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Homework(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    submission_rate = models.FloatField()  # 0-100%
    accuracy = models.FloatField()  # 0-100%


class Exam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    score = models.FloatField()  # 0-100


class ClassInteraction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    questions_asked = models.IntegerField(default=0)
    answers_given = models.IntegerField(default=0)
    answer_accuracy = models.FloatField()  # 0-100%


class StudyBehavior(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    study_hours = models.FloatField()  # 每周学习时长
    resource_usage = models.IntegerField()  # 资源使用次数