from rest_framework import serializers
from .models import (
    Department, Program, Student, Course, Enrollment,
    Attendance, Assignment, AssignmentSubmission
)

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class ProgramSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Program
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    program_name = serializers.CharField(source='program.name', read_only=True)

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    prerequisites_names = serializers.StringRelatedField(source='prerequisites', read_only=True, many=True)

    class Meta:
        model = Course
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='enrollment.student.user.get_full_name', read_only=True)
    course_name = serializers.CharField(source='enrollment.course.name', read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = Assignment
        fields = '__all__'

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = '__all__'

class StudentDashboardSerializer(serializers.Serializer):
    """Student Dashboard Summary"""
    student_info = StudentSerializer()
    current_enrollments = EnrollmentSerializer(many=True)
    upcoming_assignments = AssignmentSerializer(many=True)
    recent_attendance = AttendanceSerializer(many=True)
    academic_summary = serializers.DictField()
