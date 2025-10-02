from django.contrib import admin
from .models import (
    ExamType, Exam, QuestionBank, ExamQuestion, StudentExam,
    ExamResult, AnswerSheet, QuestionAnswer, GradingRubric
)

@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'weightage_percentage', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'exam_type', 'exam_date', 'start_time', 'total_marks', 'status')
    list_filter = ('status', 'exam_type', 'exam_date', 'course__department')
    search_fields = ('title', 'course__code', 'course__name')
    date_hierarchy = 'exam_date'

@admin.register(QuestionBank)
class QuestionBankAdmin(admin.ModelAdmin):
    list_display = ('course', 'question_type', 'difficulty_level', 'marks', 'topic', 'created_by')
    list_filter = ('question_type', 'difficulty_level', 'course', 'is_active')
    search_fields = ('question_text', 'topic', 'chapter')

@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'question_number', 'question', 'marks_allocated', 'is_mandatory')
    list_filter = ('exam__course', 'is_mandatory')
    search_fields = ('exam__title', 'question__question_text')

@admin.register(StudentExam)
class StudentExamAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'seat_number', 'status', 'registration_date')
    list_filter = ('status', 'exam__course', 'registration_date')
    search_fields = ('student__student_id', 'exam__title', 'seat_number')

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('student_exam', 'marks_obtained', 'percentage', 'grade', 'is_passed', 'status')
    list_filter = ('status', 'is_passed', 'grade', 'graded_at')
    search_fields = ('student_exam__student__student_id', 'student_exam__exam__title')

@admin.register(AnswerSheet)
class AnswerSheetAdmin(admin.ModelAdmin):
    list_display = ('student_exam', 'submission_time', 'plagiarism_score', 'is_submitted')
    list_filter = ('is_submitted', 'submission_time')
    search_fields = ('student_exam__student__student_id', 'student_exam__exam__title')

@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_sheet', 'exam_question', 'marks_awarded', 'is_correct', 'graded_by')
    list_filter = ('is_correct', 'graded_at')
    search_fields = ('answer_sheet__student_exam__student__student_id',)

@admin.register(GradingRubric)
class GradingRubricAdmin(admin.ModelAdmin):
    list_display = ('question', 'criteria', 'excellent_marks', 'good_marks', 'average_marks', 'poor_marks')
    list_filter = ('question__course',)
    search_fields = ('criteria', 'question__question_text')
