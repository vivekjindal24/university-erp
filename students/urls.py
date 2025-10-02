from django.urls import path
from . import views

urlpatterns = [
    # Department URLs
    path('departments/', views.DepartmentListCreateView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),

    # Program URLs
    path('programs/', views.ProgramListCreateView.as_view(), name='program-list-create'),

    # Student URLs
    path('', views.StudentListCreateView.as_view(), name='student-list-create'),
    path('dashboard/<int:student_id>/', views.student_dashboard, name='student-dashboard'),

    # Course URLs
    path('courses/', views.CourseListCreateView.as_view(), name='course-list-create'),

    # Enrollment URLs
    path('enrollments/', views.EnrollmentListCreateView.as_view(), name='enrollment-list-create'),

    # Attendance URLs
    path('attendance/mark/', views.mark_attendance, name='mark-attendance'),
]
