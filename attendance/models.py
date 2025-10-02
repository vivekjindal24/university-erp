from django.db import models
from students.models import Student
from courses.models import Course

class Attendance(models.Model):
    """Student Attendance Model"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10)  # Present/Absent

    def __str__(self):
        return f"{self.student.name} - {self.course.code} ({self.date})"
