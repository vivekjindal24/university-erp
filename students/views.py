from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg
from datetime import datetime, timedelta
from .models import (
    Department, Program, Student, Course, Enrollment,
    Attendance, Assignment, AssignmentSubmission
)
from .serializers import (
    DepartmentSerializer, ProgramSerializer, StudentSerializer, CourseSerializer,
    EnrollmentSerializer, AttendanceSerializer, AssignmentSerializer,
    AssignmentSubmissionSerializer, StudentDashboardSerializer
)

class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProgramListCreateView(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Program.objects.all()
        department_id = self.request.query_params.get('department', None)
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset

class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Student.objects.select_related('user', 'program')
        status_filter = self.request.query_params.get('status', None)
        program_id = self.request.query_params.get('program', None)

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if program_id:
            queryset = queryset.filter(program_id=program_id)

        return queryset

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Course.objects.select_related('department')
        department_id = self.request.query_params.get('department', None)
        semester = self.request.query_params.get('semester', None)
        year = self.request.query_params.get('year', None)

        if department_id:
            queryset = queryset.filter(department_id=department_id)
        if semester:
            queryset = queryset.filter(semester=semester)
        if year:
            queryset = queryset.filter(year=year)

        return queryset

class EnrollmentListCreateView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Enrollment.objects.select_related('student__user', 'course')
        student_id = self.request.query_params.get('student', None)
        course_id = self.request.query_params.get('course', None)

        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        return queryset

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def student_dashboard(request, student_id):
    """Student Dashboard API"""
    try:
        student = get_object_or_404(Student, id=student_id)

        # Current enrollments
        current_enrollments = Enrollment.objects.filter(
            student=student,
            status='enrolled'
        ).select_related('course')

        # Upcoming assignments
        upcoming_assignments = Assignment.objects.filter(
            course__in=[e.course for e in current_enrollments],
            due_date__gte=datetime.now()
        ).order_by('due_date')[:5]

        # Recent attendance
        recent_attendance = Attendance.objects.filter(
            enrollment__student=student,
            date__gte=datetime.now() - timedelta(days=30)
        ).order_by('-date')[:10]

        # Academic summary
        academic_summary = {
            'current_semester': student.current_semester,
            'current_year': student.current_year,
            'cgpa': float(student.cgpa),
            'total_credits': student.total_credits_earned,
            'attendance_percentage': recent_attendance.filter(status='present').count() / max(recent_attendance.count(), 1) * 100
        }

        dashboard_data = {
            'student_info': StudentSerializer(student).data,
            'current_enrollments': EnrollmentSerializer(current_enrollments, many=True).data,
            'upcoming_assignments': AssignmentSerializer(upcoming_assignments, many=True).data,
            'recent_attendance': AttendanceSerializer(recent_attendance, many=True).data,
            'academic_summary': academic_summary
        }

        return Response(dashboard_data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_attendance(request):
    """Mark Attendance API"""
    try:
        enrollment_id = request.data.get('enrollment_id')
        attendance_status = request.data.get('status')
        date = request.data.get('date', datetime.now().date())

        enrollment = get_object_or_404(Enrollment, id=enrollment_id)

        attendance, created = Attendance.objects.get_or_create(
            enrollment=enrollment,
            date=date,
            defaults={
                'status': attendance_status,
                'marked_by': request.user
            }
        )

        if not created:
            attendance.status = attendance_status
            attendance.marked_by = request.user
            attendance.save()

        return Response(AttendanceSerializer(attendance).data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
