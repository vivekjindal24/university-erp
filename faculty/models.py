from django.db import models
from django.conf import settings
from students.models import Department, Course

class Faculty(models.Model):
    """Faculty/Staff Model"""
    FACULTY_TYPES = (
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
        ('visiting_faculty', 'Visiting Faculty'),
        ('adjunct', 'Adjunct Faculty'),
    )

    EMPLOYMENT_STATUS = (
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('sabbatical', 'Sabbatical'),
        ('retired', 'Retired'),
        ('terminated', 'Terminated'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    faculty_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='faculty_members')
    faculty_type = models.CharField(max_length=30, choices=FACULTY_TYPES)
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS, default='active')
    hire_date = models.DateField()
    office_location = models.CharField(max_length=100, blank=True)
    office_hours = models.TextField(blank=True)
    research_interests = models.TextField(blank=True)
    qualifications = models.TextField()
    experience_years = models.PositiveIntegerField(default=0)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    contract_end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.faculty_id} - {self.user.get_full_name()}"

class CourseAssignment(models.Model):
    """Faculty Course Teaching Assignments"""
    SEMESTER_CHOICES = (
        ('fall', 'Fall'),
        ('spring', 'Spring'),
        ('summer', 'Summer'),
    )

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='course_assignments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='faculty_assignments')
    academic_year = models.CharField(max_length=9)  # e.g., "2023-2024"
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    section = models.CharField(max_length=10, default='A')
    student_capacity = models.PositiveIntegerField(default=30)
    room_number = models.CharField(max_length=20, blank=True)
    schedule = models.TextField(blank=True)  # JSON format for class timings
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['faculty', 'course', 'academic_year', 'semester', 'section']

    def __str__(self):
        return f"{self.faculty.faculty_id} - {self.course.code} ({self.academic_year})"

class FacultyLeave(models.Model):
    """Faculty Leave Management"""
    LEAVE_TYPES = (
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('vacation', 'Vacation'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('sabbatical', 'Sabbatical'),
        ('emergency', 'Emergency Leave'),
    )

    LEAVE_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    )

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=LEAVE_STATUS, default='pending')
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_leaves'
    )
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    substitute_faculty = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='substitute_assignments'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.faculty.faculty_id} - {self.leave_type} ({self.start_date} to {self.end_date})"

class FacultyEvaluation(models.Model):
    """Faculty Performance Evaluation"""
    EVALUATION_TYPES = (
        ('student_feedback', 'Student Feedback'),
        ('peer_review', 'Peer Review'),
        ('self_assessment', 'Self Assessment'),
        ('administrative_review', 'Administrative Review'),
    )

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='evaluations')
    evaluation_type = models.CharField(max_length=30, choices=EVALUATION_TYPES)
    academic_year = models.CharField(max_length=9)
    semester = models.CharField(max_length=10)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    overall_rating = models.DecimalField(max_digits=3, decimal_places=2)  # Out of 5.00
    teaching_effectiveness = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    research_contribution = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    service_contribution = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    comments = models.TextField(blank=True)
    evaluated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evaluation_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.faculty.faculty_id} - {self.evaluation_type} ({self.academic_year})"

class ResearchWork(models.Model):
    """Faculty Research Projects and Publications"""
    RESEARCH_TYPES = (
        ('publication', 'Publication'),
        ('conference', 'Conference'),
        ('project', 'Research Project'),
        ('grant', 'Grant'),
        ('patent', 'Patent'),
        ('book', 'Book'),
    )

    RESEARCH_STATUS = (
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('published', 'Published'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
    )

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='research_works')
    title = models.CharField(max_length=200)
    research_type = models.CharField(max_length=20, choices=RESEARCH_TYPES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=RESEARCH_STATUS)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    collaborators = models.TextField(blank=True)
    funding_agency = models.CharField(max_length=100, blank=True)
    funding_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    publication_venue = models.CharField(max_length=200, blank=True)
    doi = models.CharField(max_length=100, blank=True)
    impact_factor = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    citation_count = models.PositiveIntegerField(default=0)
    document = models.FileField(upload_to='research_documents/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.faculty.faculty_id} - {self.title}"

class FacultyWorkload(models.Model):
    """Faculty Teaching and Administrative Workload"""
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='workloads')
    academic_year = models.CharField(max_length=9)
    semester = models.CharField(max_length=10)
    teaching_hours_per_week = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    research_hours_per_week = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    administrative_hours_per_week = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_courses = models.PositiveIntegerField(default=0)
    total_students = models.PositiveIntegerField(default=0)
    committee_memberships = models.TextField(blank=True)
    administrative_roles = models.TextField(blank=True)
    overload_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overload_compensation = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['faculty', 'academic_year', 'semester']

    def __str__(self):
        return f"{self.faculty.faculty_id} - Workload ({self.academic_year} {self.semester})"
