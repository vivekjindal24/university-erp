from django.db import models
from departments.models import Department

class Course(models.Model):
    """Course Model"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    credits = models.PositiveIntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    faculty_assigned = models.ManyToManyField('faculty.Faculty', related_name='courses_assigned', blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

