from django.db import models
from students.models import Student
from faculty.models import Faculty

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    quantity_total = models.PositiveIntegerField()
    quantity_available = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} ({self.isbn})"

class BookIssue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='library_issues')
    issued_to_student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.SET_NULL, related_name='library_book_issues')
    issued_to_faculty = models.ForeignKey(Faculty, null=True, blank=True, on_delete=models.SET_NULL, related_name='library_book_issues')
    issue_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} issued"
