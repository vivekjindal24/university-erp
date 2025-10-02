from departments.models import Department
from courses.models import Course
from faculty.models import Faculty
from students.models import Student
from exams.models import Exam
from results.models import Result
from admissions.models import Admission
from fees.models import Fee
from attendance.models import Attendance
from library.models import Book, BookIssue
from hostel.models import Hostel, HostelRoom, HostelAllocation
from payroll.models import Payroll
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

# Departments
cs = Department.objects.create(name="Computer Science", head_of_department="Dr. Smith")
ee = Department.objects.create(name="Electrical Engineering", head_of_department="Dr. Jones")

# Courses
algorithms = Course.objects.create(name="Algorithms", code="CS101", credits=4, department=cs)
circuits = Course.objects.create(name="Circuits", code="EE101", credits=3, department=ee)

# Faculty Users
user_alice = User.objects.create(username="alice", first_name="Alice", last_name="Anderson", email="alice@uni.edu")
user_bob = User.objects.create(username="bob", first_name="Bob", last_name="Brown", email="bob@uni.edu")

# Faculty
alice = Faculty.objects.create(user=user_alice, faculty_id="F001", department=cs, faculty_type="professor", employment_status="active", hire_date=date(2020, 8, 1), qualifications="PhD", experience_years=10, salary=90000)
bob = Faculty.objects.create(user=user_bob, faculty_id="F002", department=ee, faculty_type="lecturer", employment_status="active", hire_date=date(2021, 8, 1), qualifications="MTech", experience_years=5, salary=60000)
alice.courses_assigned.add(algorithms)
bob.courses_assigned.add(circuits)

# Students
student_john = Student.objects.create(name="John Doe", email="john@uni.edu", phone="1234567890", address="123 Main St", department=cs, degree_status="Active")
student_jane = Student.objects.create(name="Jane Roe", email="jane@uni.edu", phone="0987654321", address="456 Elm St", department=ee, degree_status="Active")
student_john.courses_enrolled.add(algorithms)
student_jane.courses_enrolled.add(circuits)

# Exams
exam_alg_mid = Exam.objects.create(name="Midterm", date=date(2025, 10, 10), course=algorithms, max_marks=100)
exam_circ_final = Exam.objects.create(name="Final", date=date(2025, 12, 15), course=circuits, max_marks=100)

# Results
Result.objects.create(student=student_john, exam=exam_alg_mid, marks_obtained=85, grade="A")
Result.objects.create(student=student_jane, exam=exam_circ_final, marks_obtained=78, grade="B")

# Admissions
Admission.objects.create(applicant_name="Sam Smith", email="sam@uni.edu", status="Accepted", documents="Transcript", fees_paid=True)

# Fees
Fee.objects.create(student=student_john, semester="Fall 2025", amount_due=5000, amount_paid=5000, due_date=date(2025, 9, 1))
Fee.objects.create(student=student_jane, semester="Fall 2025", amount_due=5000, amount_paid=2500, due_date=date(2025, 9, 1))

# Attendance
Attendance.objects.create(student=student_john, course=algorithms, date=date(2025, 10, 1), status="Present")
Attendance.objects.create(student=student_jane, course=circuits, date=date(2025, 10, 1), status="Absent")

# Library
book_python = Book.objects.create(title="Python Programming", author="Guido", isbn="123456789", quantity_total=5, quantity_available=5)
BookIssue.objects.create(book=book_python, issued_to_student=student_john, issue_date=date(2025, 9, 15), return_date=date(2025, 9, 30))

# Hostel
hostel_a = Hostel.objects.create(name="A Block", total_rooms=50, fees=2000)
room_101 = HostelRoom.objects.create(hostel=hostel_a, room_number="101", capacity=2)
HostelAllocation.objects.create(student=student_john, room=room_101, allocation_date=date(2025, 8, 1))

# Payroll
Payroll.objects.create(faculty=alice, department=cs, salary=90000, leave=2, pay_date=date(2025, 9, 30))
Payroll.objects.create(faculty=bob, department=ee, salary=60000, leave=1, pay_date=date(2025, 9, 30))

