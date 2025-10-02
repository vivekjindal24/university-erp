from rest_framework import serializers
from .models import (
    Faculty, CourseAssignment, FacultyLeave, FacultyEvaluation,
    ResearchWork, FacultyWorkload
)

class FacultySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Faculty
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class CourseAssignmentSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.user.get_full_name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = CourseAssignment
        fields = '__all__'

class FacultyLeaveSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.user.get_full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)

    class Meta:
        model = FacultyLeave
        fields = '__all__'

class FacultyEvaluationSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.user.get_full_name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = FacultyEvaluation
        fields = '__all__'

class ResearchWorkSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.user.get_full_name', read_only=True)

    class Meta:
        model = ResearchWork
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class FacultyWorkloadSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.user.get_full_name', read_only=True)

    class Meta:
        model = FacultyWorkload
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
