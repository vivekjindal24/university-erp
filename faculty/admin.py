from django.contrib import admin
from .models import (
    Faculty, CourseAssignment, FacultyLeave, FacultyEvaluation,
    ResearchWork, FacultyWorkload
)

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('faculty_id', 'user', 'department', 'faculty_type', 'employment_status', 'hire_date')
    list_filter = ('faculty_type', 'employment_status', 'department', 'hire_date')
    search_fields = ('faculty_id', 'user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CourseAssignment)
class CourseAssignmentAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'course', 'academic_year', 'semester', 'section', 'is_active')
    list_filter = ('academic_year', 'semester', 'is_active', 'course__department')
    search_fields = ('faculty__faculty_id', 'course__code', 'course__name')

@admin.register(FacultyLeave)
class FacultyLeaveAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'leave_type', 'start_date', 'end_date', 'status', 'approved_by')
    list_filter = ('leave_type', 'status', 'start_date')
    search_fields = ('faculty__faculty_id', 'faculty__user__first_name', 'faculty__user__last_name')
    date_hierarchy = 'start_date'

@admin.register(FacultyEvaluation)
class FacultyEvaluationAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'evaluation_type', 'academic_year', 'semester', 'overall_rating', 'evaluation_date')
    list_filter = ('evaluation_type', 'academic_year', 'semester')
    search_fields = ('faculty__faculty_id', 'faculty__user__first_name', 'faculty__user__last_name')

@admin.register(ResearchWork)
class ResearchWorkAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'title', 'research_type', 'status', 'start_date')
    list_filter = ('research_type', 'status', 'start_date')
    search_fields = ('faculty__faculty_id', 'title', 'faculty__user__first_name')
    date_hierarchy = 'start_date'

@admin.register(FacultyWorkload)
class FacultyWorkloadAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'academic_year', 'semester', 'total_courses', 'total_students', 'teaching_hours_per_week')
    list_filter = ('academic_year', 'semester')
    search_fields = ('faculty__faculty_id', 'faculty__user__first_name', 'faculty__user__last_name')
