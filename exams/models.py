from django.db import models
from django.conf import settings
from students.models import Course, Student, Enrollment
from faculty.models import Faculty

class ExamType(models.Model):
    """Types of Examinations"""
    name = models.CharField(max_length=50, unique=True)  # e.g., "Midterm", "Final", "Quiz"
    description = models.TextField(blank=True)
    weightage_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Out of 100
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Exam(models.Model):
    """Examination Schedule and Details"""
    EXAM_STATUS = (
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('postponed', 'Postponed'),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    academic_year = models.CharField(max_length=9)
    semester = models.CharField(max_length=10)
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    passing_marks = models.PositiveIntegerField()
    room_number = models.CharField(max_length=20)
    invigilator = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='invigilated_exams')
    status = models.CharField(max_length=20, choices=EXAM_STATUS, default='scheduled')
    instructions = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.code} - {self.exam_type.name} ({self.exam_date})"

class QuestionBank(models.Model):
    """Question Bank for Examinations"""
    QUESTION_TYPES = (
        ('mcq', 'Multiple Choice'),
        ('short_answer', 'Short Answer'),
        ('long_answer', 'Long Answer'),
        ('true_false', 'True/False'),
        ('fill_blank', 'Fill in the Blank'),
        ('numerical', 'Numerical'),
        ('essay', 'Essay'),
    )

    DIFFICULTY_LEVELS = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='question_bank')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS)
    marks = models.PositiveIntegerField()
    option_a = models.TextField(blank=True)
    option_b = models.TextField(blank=True)
    option_c = models.TextField(blank=True)
    option_d = models.TextField(blank=True)
    correct_answer = models.TextField()
    explanation = models.TextField(blank=True)
    topic = models.CharField(max_length=100, blank=True)
    chapter = models.CharField(max_length=100, blank=True)
    learning_outcome = models.TextField(blank=True)
    created_by = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.code} - {self.question_type} - {self.marks} marks"

class ExamQuestion(models.Model):
    """Questions included in a specific exam"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_questions')
    question = models.ForeignKey(QuestionBank, on_delete=models.CASCADE)
    question_number = models.PositiveIntegerField()
    marks_allocated = models.PositiveIntegerField()
    is_mandatory = models.BooleanField(default=True)

    class Meta:
        unique_together = ['exam', 'question_number']
        ordering = ['question_number']

    def __str__(self):
        return f"{self.exam.title} - Q{self.question_number}"

class StudentExam(models.Model):
    """Student Exam Registration and Status"""
    EXAM_STATUS = (
        ('registered', 'Registered'),
        ('appeared', 'Appeared'),
        ('absent', 'Absent'),
        ('disqualified', 'Disqualified'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_exams')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='student_registrations')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=20, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=EXAM_STATUS, default='registered')
    attendance_marked_at = models.DateTimeField(null=True, blank=True)
    special_requirements = models.TextField(blank=True)

    class Meta:
        unique_together = ['student', 'exam']

    def __str__(self):
        return f"{self.student.student_id} - {self.exam.title}"

class ExamResult(models.Model):
    """Exam Results and Grades"""
    RESULT_STATUS = (
        ('pending', 'Pending'),
        ('graded', 'Graded'),
        ('published', 'Published'),
        ('under_review', 'Under Review'),
    )

    student_exam = models.OneToOneField(StudentExam, on_delete=models.CASCADE, related_name='result')
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=5)
    grade_points = models.DecimalField(max_digits=4, decimal_places=2)
    is_passed = models.BooleanField()
    rank_in_class = models.PositiveIntegerField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=RESULT_STATUS, default='pending')
    graded_by = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    graded_at = models.DateTimeField()
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_exam.student.student_id} - {self.student_exam.exam.title} - {self.grade}"

class AnswerSheet(models.Model):
    """Digital Answer Sheets"""
    student_exam = models.OneToOneField(StudentExam, on_delete=models.CASCADE, related_name='answer_sheet')
    answer_file = models.FileField(upload_to='answer_sheets/', blank=True, null=True)
    submission_time = models.DateTimeField(null=True, blank=True)
    auto_save_data = models.JSONField(default=dict, blank=True)  # For online exams
    plagiarism_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_submitted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Answer Sheet - {self.student_exam.student.student_id} - {self.student_exam.exam.title}"

class QuestionAnswer(models.Model):
    """Individual Question Answers and Grading"""
    answer_sheet = models.ForeignKey(AnswerSheet, on_delete=models.CASCADE, related_name='question_answers')
    exam_question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
    selected_option = models.CharField(max_length=1, blank=True)  # For MCQs
    marks_awarded = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_correct = models.BooleanField(null=True, blank=True)
    grader_comments = models.TextField(blank=True)
    graded_by = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True)
    graded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['answer_sheet', 'exam_question']

    def __str__(self):
        return f"{self.answer_sheet.student_exam.student.student_id} - Q{self.exam_question.question_number}"

class GradingRubric(models.Model):
    """Grading Rubrics for Subjective Questions"""
    question = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, related_name='rubrics')
    criteria = models.CharField(max_length=200)
    excellent_description = models.TextField()
    good_description = models.TextField()
    average_description = models.TextField()
    poor_description = models.TextField()
    excellent_marks = models.DecimalField(max_digits=4, decimal_places=2)
    good_marks = models.DecimalField(max_digits=4, decimal_places=2)
    average_marks = models.DecimalField(max_digits=4, decimal_places=2)
    poor_marks = models.DecimalField(max_digits=4, decimal_places=2)
    created_by = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question.course.code} - {self.criteria}"
