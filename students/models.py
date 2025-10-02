from django.db import models
from django.conf import settings

class Department(models.Model):
    """University Departments"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    head_of_department = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_departments'
    )
    established_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Program(models.Model):
    """Academic Programs (Courses like BSc, MSc, PhD)"""
    PROGRAM_TYPES = (
        ('undergraduate', 'Undergraduate'),
        ('postgraduate', 'Postgraduate'),
        ('doctoral', 'Doctoral'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    )

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programs')
    duration_years = models.PositiveIntegerField()
    total_credits = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    fees_per_semester = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Student(models.Model):
    """Student Model"""
    STUDENT_STATUS = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
        ('dropped', 'Dropped'),
        ('suspended', 'Suspended'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='students')
    enrollment_date = models.DateField()
    expected_graduation_date = models.DateField()
    current_semester = models.PositiveIntegerField(default=1)
    current_year = models.PositiveIntegerField(default=1)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    total_credits_earned = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STUDENT_STATUS, default='active')
    guardian_name = models.CharField(max_length=100)
    guardian_contact = models.CharField(max_length=15)
    guardian_email = models.EmailField()
    blood_group = models.CharField(max_length=5, blank=True)
    medical_conditions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"

class Course(models.Model):
    """Individual Courses/Subjects"""
    COURSE_TYPES = (
        ('core', 'Core'),
        ('elective', 'Elective'),
        ('minor', 'Minor'),
        ('project', 'Project'),
    )

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    credits = models.PositiveIntegerField()
    course_type = models.CharField(max_length=20, choices=COURSE_TYPES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    semester = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Enrollment(models.Model):
    """Student Course Enrollment"""
    ENROLLMENT_STATUS = (
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('failed', 'Failed'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    semester = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ENROLLMENT_STATUS, default='enrolled')
    grade = models.CharField(max_length=5, blank=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'course', 'semester', 'year']

    def __str__(self):
        return f"{self.student.student_id} - {self.course.code}"

class Attendance(models.Model):
    """Student Attendance Records"""
    ATTENDANCE_STATUS = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    )

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS)
    remarks = models.TextField(blank=True)
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['enrollment', 'date']

    def __str__(self):
        return f"{self.enrollment.student.student_id} - {self.date} - {self.status}"

class Assignment(models.Model):
    """Course Assignments"""
    ASSIGNMENT_TYPES = (
        ('homework', 'Homework'),
        ('project', 'Project'),
        ('quiz', 'Quiz'),
        ('lab', 'Lab Work'),
        ('presentation', 'Presentation'),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    assignment_type = models.CharField(max_length=20, choices=ASSIGNMENT_TYPES)
    total_marks = models.PositiveIntegerField()
    due_date = models.DateTimeField()
    submission_format = models.CharField(max_length=100, blank=True)
    attachment = models.FileField(upload_to='assignments/', blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.code} - {self.title}"

class AssignmentSubmission(models.Model):
    """Student Assignment Submissions"""
    SUBMISSION_STATUS = (
        ('submitted', 'Submitted'),
        ('late', 'Late Submission'),
        ('graded', 'Graded'),
        ('pending', 'Pending'),
    )

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    submission_file = models.FileField(upload_to='submissions/')
    submission_text = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=SUBMISSION_STATUS, default='submitted')
    marks_obtained = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    graded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    graded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['assignment', 'student']

    def __str__(self):
        return f"{self.student.student_id} - {self.assignment.title}"
