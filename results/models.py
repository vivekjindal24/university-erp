from django.db import models
from students.models import Student
from exams.models import Exam

class Result(models.Model):
    """Exam Results for Students"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='student_results')
    marks_obtained = models.FloatField()
    grade = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.student.student_id} - {self.exam.title} ({self.grade})"
