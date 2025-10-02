from django.contrib import admin
from .models import (
    Department, Program, Student, Course, Enrollment,
    Attendance, Assignment, AssignmentSubmission
)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'head_of_department', 'established_date', 'is_active')
    list_filter = ('is_active', 'established_date')
    search_fields = ('name', 'code')
    date_hierarchy = 'established_date'

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'program_type', 'department', 'duration_years', 'fees_per_semester', 'is_active')
    list_filter = ('program_type', 'department', 'is_active')
    search_fields = ('name', 'code')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user', 'program', 'current_semester', 'cgpa', 'status')
    list_filter = ('status', 'program', 'current_semester')
    search_fields = ('student_id', 'user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'credits', 'course_type', 'department', 'semester', 'year', 'is_active')
    list_filter = ('course_type', 'department', 'semester', 'year', 'is_active')
    search_fields = ('code', 'name')
    filter_horizontal = ('prerequisites',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'semester', 'year', 'status', 'grade', 'gpa')
    list_filter = ('status', 'semester', 'year', 'course__department')
    search_fields = ('student__student_id', 'course__code', 'course__name')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'date', 'status', 'marked_by')
    list_filter = ('status', 'date', 'enrollment__course__department')
    search_fields = ('enrollment__student__student_id', 'enrollment__course__code')
    date_hierarchy = 'date'

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'assignment_type', 'total_marks', 'due_date', 'created_by')
    list_filter = ('assignment_type', 'course__department', 'due_date')
    search_fields = ('title', 'course__code', 'course__name')
    date_hierarchy = 'due_date'

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'status', 'marks_obtained', 'submitted_at')
    list_filter = ('status', 'assignment__assignment_type', 'submitted_at')
    search_fields = ('student__student_id', 'assignment__title')
    date_hierarchy = 'submitted_at'
