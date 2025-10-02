from django.db import models
from django.conf import settings
from students.models import Program, Department

class AdmissionCycle(models.Model):
    """Admission Cycles for different academic years"""
    name = models.CharField(max_length=100)  # e.g., "Fall 2024 Admissions"
    academic_year = models.CharField(max_length=9)  # e.g., "2024-2025"
    application_start_date = models.DateField()
    application_end_date = models.DateField()
    entrance_exam_date = models.DateField(null=True, blank=True)
    interview_start_date = models.DateField(null=True, blank=True)
    interview_end_date = models.DateField(null=True, blank=True)
    result_announcement_date = models.DateField(null=True, blank=True)
    admission_confirmation_deadline = models.DateField(null=True, blank=True)
    session_start_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.academic_year})"

class AdmissionRequirement(models.Model):
    """Admission Requirements for Programs"""
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='admission_requirements')
    admission_cycle = models.ForeignKey(AdmissionCycle, on_delete=models.CASCADE)
    minimum_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    entrance_exam_required = models.BooleanField(default=False)
    interview_required = models.BooleanField(default=False)
    portfolio_required = models.BooleanField(default=False)
    work_experience_required = models.BooleanField(default=False)
    minimum_work_experience_months = models.PositiveIntegerField(default=0)
    required_subjects = models.TextField(blank=True)  # JSON format
    additional_requirements = models.TextField(blank=True)
    application_fee = models.DecimalField(max_digits=8, decimal_places=2)
    total_seats = models.PositiveIntegerField()
    reserved_seats_sc = models.PositiveIntegerField(default=0)
    reserved_seats_st = models.PositiveIntegerField(default=0)
    reserved_seats_obc = models.PositiveIntegerField(default=0)
    reserved_seats_pwd = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['program', 'admission_cycle']

    def __str__(self):
        return f"{self.program.name} - {self.admission_cycle.name}"

class Applicant(models.Model):
    """Prospective Students/Applicants"""
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    CATEGORY_CHOICES = (
        ('general', 'General'),
        ('sc', 'Scheduled Caste'),
        ('st', 'Scheduled Tribe'),
        ('obc', 'Other Backward Class'),
        ('pwd', 'Person with Disability'),
    )

    # Personal Information
    application_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=50, default='Indian')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    # Address Information
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default='India')

    # Guardian Information
    guardian_name = models.CharField(max_length=100)
    guardian_relation = models.CharField(max_length=50)
    guardian_phone = models.CharField(max_length=15)
    guardian_email = models.EmailField(blank=True)
    guardian_occupation = models.CharField(max_length=100, blank=True)
    guardian_annual_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Profile Photo
    profile_photo = models.ImageField(upload_to='applicant_photos/', blank=True, null=True)

    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.application_number} - {self.first_name} {self.last_name}"

class Application(models.Model):
    """Student Applications"""
    APPLICATION_STATUS = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('selected', 'Selected'),
        ('waitlisted', 'Waitlisted'),
        ('rejected', 'Rejected'),
        ('admitted', 'Admitted'),
        ('cancelled', 'Cancelled'),
    )

    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='applications')
    admission_cycle = models.ForeignKey(AdmissionCycle, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=APPLICATION_STATUS, default='draft')
    application_date = models.DateTimeField(auto_now_add=True)
    submission_date = models.DateTimeField(null=True, blank=True)
    application_fee_paid = models.BooleanField(default=False)
    application_fee_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    payment_reference = models.CharField(max_length=100, blank=True)

    # Admission Decision Fields
    admission_decision = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('admitted', 'Admitted'),
        ('not_admitted', 'Not Admitted')
    ], default='pending')
    admission_decision_date = models.DateTimeField(null=True, blank=True)
    admission_decision_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='admission_decisions')
    admission_letter_generated = models.BooleanField(default=False)
    admission_letter_generated_date = models.DateTimeField(null=True, blank=True)

    # First Semester Fee Payment
    first_semester_fee_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    first_semester_fee_paid = models.BooleanField(default=False)
    first_semester_fee_payment_date = models.DateTimeField(null=True, blank=True)
    first_semester_fee_transaction_id = models.CharField(max_length=100, blank=True)

    # Academic Information
    previous_school_name = models.CharField(max_length=200)
    previous_school_board = models.CharField(max_length=100)
    graduation_year = models.PositiveIntegerField()
    overall_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    # Entrance Exam
    entrance_exam_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    entrance_exam_rank = models.PositiveIntegerField(null=True, blank=True)

    # Interview
    interview_date = models.DateTimeField(null=True, blank=True)
    interview_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    interview_feedback = models.TextField(blank=True)

    # Selection
    merit_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    merit_rank = models.PositiveIntegerField(null=True, blank=True)
    waitlist_number = models.PositiveIntegerField(null=True, blank=True)

    # Additional Information
    statement_of_purpose = models.TextField(blank=True)
    extracurricular_activities = models.TextField(blank=True)
    work_experience = models.TextField(blank=True)

    # Review Information
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    review_date = models.DateTimeField(null=True, blank=True)
    review_comments = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['applicant', 'admission_cycle', 'program']

    def __str__(self):
        return f"{self.applicant.application_number} - {self.program.name}"

class ApplicationDocument(models.Model):
    """Documents uploaded by applicants"""
    DOCUMENT_TYPES = (
        ('photo', 'Passport Size Photo'),
        ('signature', 'Signature'),
        ('10th_certificate', '10th Grade Certificate'),
        ('12th_certificate', '12th Grade Certificate'),
        ('graduation_certificate', 'Graduation Certificate'),
        ('postgraduation_certificate', 'Post-graduation Certificate'),
        ('transcript', 'Academic Transcript'),
        ('caste_certificate', 'Caste Certificate'),
        ('income_certificate', 'Income Certificate'),
        ('migration_certificate', 'Migration Certificate'),
        ('character_certificate', 'Character Certificate'),
        ('experience_certificate', 'Experience Certificate'),
        ('portfolio', 'Portfolio'),
        ('other', 'Other'),
    )

    VERIFICATION_STATUS = (
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('resubmission_required', 'Resubmission Required'),
    )

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to='application_documents/')
    document_name = models.CharField(max_length=200)
    is_mandatory = models.BooleanField(default=True)
    verification_status = models.CharField(max_length=30, choices=VERIFICATION_STATUS, default='pending')
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    verification_date = models.DateTimeField(null=True, blank=True)
    verification_comments = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application.applicant.application_number} - {self.get_document_type_display()}"

class AdmissionTest(models.Model):
    """Entrance Tests and Interviews"""
    TEST_TYPES = (
        ('entrance_exam', 'Entrance Examination'),
        ('aptitude_test', 'Aptitude Test'),
        ('interview', 'Personal Interview'),
        ('group_discussion', 'Group Discussion'),
        ('portfolio_review', 'Portfolio Review'),
    )

    admission_cycle = models.ForeignKey(AdmissionCycle, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    test_type = models.CharField(max_length=30, choices=TEST_TYPES)
    test_name = models.CharField(max_length=200)
    test_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    venue = models.CharField(max_length=200)
    instructions = models.TextField(blank=True)
    syllabus = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test_name} - {self.program.name} ({self.test_date})"

class TestRegistration(models.Model):
    """Test Registration for Applicants"""
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='test_registrations')
    test = models.ForeignKey(AdmissionTest, on_delete=models.CASCADE, related_name='registrations')
    admit_card_number = models.CharField(max_length=50, unique=True)
    seat_number = models.CharField(max_length=20, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_appeared = models.BooleanField(default=False)

    class Meta:
        unique_together = ['application', 'test']

    def __str__(self):
        return f"{self.application.applicant.application_number} - {self.test.test_name}"

class TestResult(models.Model):
    """Test Results for Applicants"""
    test_registration = models.OneToOneField(TestRegistration, on_delete=models.CASCADE, related_name='result')
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    rank = models.PositiveIntegerField(null=True, blank=True)
    grade = models.CharField(max_length=5, blank=True)
    remarks = models.TextField(blank=True)
    result_published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test_registration.application.applicant.application_number} - {self.test_registration.test.test_name} - {self.marks_obtained}"

class AdmissionFee(models.Model):
    """Admission Fee Structure and Payments"""
    FEE_TYPES = (
        ('application_fee', 'Application Fee'),
        ('admission_fee', 'Admission Fee'),
        ('security_deposit', 'Security Deposit'),
        ('tuition_fee', 'Tuition Fee'),
        ('development_fee', 'Development Fee'),
        ('library_fee', 'Library Fee'),
        ('lab_fee', 'Laboratory Fee'),
        ('hostel_fee', 'Hostel Fee'),
        ('other', 'Other'),
    )

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='fee_payments')
    fee_type = models.CharField(max_length=30, choices=FEE_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    is_paid = models.BooleanField(default=False)
    receipt_number = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application.applicant.application_number} - {self.get_fee_type_display()} - {self.amount}"
