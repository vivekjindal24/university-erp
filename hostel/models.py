from django.db import models
from students.models import Student

class Hostel(models.Model):
    name = models.CharField(max_length=100)
    total_rooms = models.PositiveIntegerField()
    fees = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class HostelRoom(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"

class HostelAllocation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='hostel_room_allocations')
    room = models.ForeignKey(HostelRoom, on_delete=models.CASCADE, related_name='allocations')
    allocation_date = models.DateField()
    checkout_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.student_id} - {self.room.room_number}"
