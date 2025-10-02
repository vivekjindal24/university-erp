from django.urls import path
from . import views

urlpatterns = [
    # Faculty URLs
    path('', views.FacultyListCreateView.as_view(), name='faculty-list-create'),
    path('<int:pk>/', views.FacultyDetailView.as_view(), name='faculty-detail'),

    # Course Assignment URLs
    path('assignments/', views.CourseAssignmentListView.as_view(), name='course-assignment-list'),
    path('assignments/create/', views.CourseAssignmentCreateView.as_view(), name='course-assignment-create'),

    # Leave Management URLs
    path('leaves/', views.FacultyLeaveListCreateView.as_view(), name='faculty-leave-list-create'),
    path('leaves/<int:pk>/', views.FacultyLeaveDetailView.as_view(), name='faculty-leave-detail'),

    # Evaluation URLs
    path('evaluations/', views.FacultyEvaluationListView.as_view(), name='faculty-evaluation-list'),

    # Research URLs
    path('research/', views.ResearchWorkListCreateView.as_view(), name='research-work-list-create'),
]
