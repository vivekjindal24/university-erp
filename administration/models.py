from django.db import models
from django.conf import settings
from students.models import Student, Department, Program
from faculty.models import Faculty

class Announcement(models.Model):
    """University Announcements and Notices"""
    ANNOUNCEMENT_TYPES = (
        ('general', 'General'),
        ('academic', 'Academic'),
        ('exam', 'Examination'),
        ('admission', 'Admission'),
        ('event', 'Event'),
        ('holiday', 'Holiday'),
        ('urgent', 'Urgent'),
    )

    TARGET_AUDIENCE = (
        ('all', 'All Users'),
        ('students', 'Students Only'),
        ('faculty', 'Faculty Only'),
        ('staff', 'Staff Only'),
        ('department', 'Specific Department'),
        ('program', 'Specific Program'),
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    announcement_type = models.CharField(max_length=20, choices=ANNOUNCEMENT_TYPES)
    target_audience = models.CharField(max_length=20, choices=TARGET_AUDIENCE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, blank=True)
    priority = models.PositiveIntegerField(default=1)  # 1=Low, 2=Medium, 3=High
    is_active = models.BooleanField(default=True)
    publish_date = models.DateTimeField()
    expiry_date = models.DateTimeField(null=True, blank=True)
    attachment = models.FileField(upload_to='announcements/', blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', '-publish_date']

    def __str__(self):
        return f"{self.title} - {self.get_announcement_type_display()}"

class Committee(models.Model):
    """University Committees"""
    COMMITTEE_TYPES = (
        ('academic', 'Academic Committee'),
        ('disciplinary', 'Disciplinary Committee'),
        ('recruitment', 'Recruitment Committee'),
        ('examination', 'Examination Committee'),
        ('research', 'Research Committee'),
        ('grievance', 'Grievance Committee'),
        ('sports', 'Sports Committee'),
        ('cultural', 'Cultural Committee'),
        ('library', 'Library Committee'),
        ('finance', 'Finance Committee'),
    )

    name = models.CharField(max_length=200)
    committee_type = models.CharField(max_length=20, choices=COMMITTEE_TYPES)
    description = models.TextField(blank=True)
    chairperson = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='chaired_committees'
    )
    establishment_date = models.DateField()
    is_active = models.BooleanField(default=True)
    meeting_frequency = models.CharField(max_length=50, blank=True)  # e.g., "Monthly", "Quarterly"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CommitteeMember(models.Model):
    """Committee Membership"""
    MEMBER_ROLES = (
        ('chairperson', 'Chairperson'),
        ('vice_chairperson', 'Vice Chairperson'),
        ('secretary', 'Secretary'),
        ('member', 'Member'),
        ('advisor', 'Advisor'),
    )

    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=MEMBER_ROLES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['committee', 'user', 'start_date']

    def __str__(self):
        return f"{self.committee.name} - {self.user.get_full_name()} ({self.role})"

class Meeting(models.Model):
    """Committee Meetings"""
    MEETING_STATUS = (
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('postponed', 'Postponed'),
    )

    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name='meetings')
    title = models.CharField(max_length=200)
    agenda = models.TextField()
    meeting_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    venue = models.CharField(max_length=200)
    meeting_link = models.URLField(blank=True)  # For online meetings
    status = models.CharField(max_length=20, choices=MEETING_STATUS, default='scheduled')
    minutes = models.TextField(blank=True)
    action_items = models.TextField(blank=True)
    next_meeting_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.committee.name} - {self.title} ({self.meeting_date.date()})"

class MeetingAttendance(models.Model):
    """Meeting Attendance Tracking"""
    ATTENDANCE_STATUS = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    )

    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='attendance_records')
    member = models.ForeignKey(CommitteeMember, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS)
    arrival_time = models.TimeField(null=True, blank=True)
    departure_time = models.TimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['meeting', 'member']

    def __str__(self):
        return f"{self.meeting.title} - {self.member.user.get_full_name()} - {self.status}"

class Policy(models.Model):
    """University Policies and Regulations"""
    POLICY_TYPES = (
        ('academic', 'Academic Policy'),
        ('administrative', 'Administrative Policy'),
        ('disciplinary', 'Disciplinary Policy'),
        ('hr', 'HR Policy'),
        ('finance', 'Finance Policy'),
        ('examination', 'Examination Policy'),
        ('admission', 'Admission Policy'),
        ('research', 'Research Policy'),
    )

    POLICY_STATUS = (
        ('draft', 'Draft'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('revised', 'Revised'),
        ('archived', 'Archived'),
    )

    title = models.CharField(max_length=200)
    policy_number = models.CharField(max_length=50, unique=True)
    policy_type = models.CharField(max_length=20, choices=POLICY_TYPES)
    description = models.TextField()
    content = models.TextField()
    version = models.CharField(max_length=10, default='1.0')
    status = models.CharField(max_length=20, choices=POLICY_STATUS, default='draft')
    effective_date = models.DateField()
    review_date = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_policies'
    )
    approval_date = models.DateTimeField(null=True, blank=True)
    document_file = models.FileField(upload_to='policies/', blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Policies'

    def __str__(self):
        return f"{self.policy_number} - {self.title}"

class Grievance(models.Model):
    """Student and Staff Grievances"""
    GRIEVANCE_TYPES = (
        ('academic', 'Academic Issue'),
        ('administrative', 'Administrative Issue'),
        ('financial', 'Financial Issue'),
        ('disciplinary', 'Disciplinary Issue'),
        ('harassment', 'Harassment'),
        ('discrimination', 'Discrimination'),
        ('facility', 'Facility Issue'),
        ('other', 'Other'),
    )

    GRIEVANCE_STATUS = (
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('escalated', 'Escalated'),
    )

    PRIORITY_LEVELS = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )

    grievance_id = models.CharField(max_length=20, unique=True)
    complainant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='filed_grievances')
    grievance_type = models.CharField(max_length=20, choices=GRIEVANCE_TYPES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')
    status = models.CharField(max_length=20, choices=GRIEVANCE_STATUS, default='submitted')
    supporting_documents = models.FileField(upload_to='grievances/', blank=True, null=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_grievances'
    )
    resolution = models.TextField(blank=True)
    resolution_date = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_grievances'
    )
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.grievance_id} - {self.subject}"

class Report(models.Model):
    """Administrative Reports"""
    REPORT_TYPES = (
        ('enrollment', 'Enrollment Report'),
        ('attendance', 'Attendance Report'),
        ('academic_performance', 'Academic Performance Report'),
        ('financial', 'Financial Report'),
        ('faculty_performance', 'Faculty Performance Report'),
        ('research', 'Research Report'),
        ('placement', 'Placement Report'),
        ('infrastructure', 'Infrastructure Report'),
        ('custom', 'Custom Report'),
    )

    REPORT_STATUS = (
        ('generating', 'Generating'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=30, choices=REPORT_TYPES)
    description = models.TextField(blank=True)
    parameters = models.JSONField(default=dict)  # Report parameters/filters
    status = models.CharField(max_length=20, choices=REPORT_STATUS, default='generating')
    file_path = models.CharField(max_length=500, blank=True)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    download_count = models.PositiveIntegerField(default=0)
    is_scheduled = models.BooleanField(default=False)
    schedule_frequency = models.CharField(max_length=20, blank=True)  # daily, weekly, monthly

    def __str__(self):
        return f"{self.title} - {self.generated_at.date()}"

class AuditLog(models.Model):
    """System Audit Logs"""
    ACTION_TYPES = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('view', 'View'),
        ('download', 'Download'),
        ('export', 'Export'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=50, blank=True)
    object_repr = models.CharField(max_length=200, blank=True)
    changes = models.JSONField(default=dict, blank=True)  # Field changes
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} - {self.action_type} - {self.model_name} ({self.timestamp})"
