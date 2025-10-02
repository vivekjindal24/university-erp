from django.db import models
from students.models import Student

class Fee(models.Model):
    """Student Fee Model"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    semester = models.CharField(max_length=20)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.student.name} - {self.semester}"

