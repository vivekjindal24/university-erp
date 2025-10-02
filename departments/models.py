from django.db import models

class Department(models.Model):
    """Department Model"""
    name = models.CharField(max_length=100, unique=True)
    head_of_department = models.CharField(max_length=100)

    def __str__(self):
        return self.name

