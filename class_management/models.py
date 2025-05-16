from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=50, default='未设置')
    subject = models.CharField(max_length=50, default='未设置')
    permission_view_scores = models.BooleanField(default=False)
    homework_deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50, unique=True)
    class_info = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField(max_length=100)
    time = models.DateTimeField()
    location = models.CharField(max_length=100)
    participants = models.ManyToManyField(Student, related_name='activities')
    class_info = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='activities')

    def __str__(self):
        return self.name