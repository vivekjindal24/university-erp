from django.db import models
from faculty.models import Faculty
from departments.models import Department

class Payroll(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='payrolls')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='payrolls')
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    leave = models.PositiveIntegerField(default=0)
    pay_date = models.DateField()

    def __str__(self):
        return f"{self.faculty.user.get_full_name()} - {self.pay_date}"

