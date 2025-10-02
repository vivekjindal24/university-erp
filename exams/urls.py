from django.urls import path
from . import views

urlpatterns = [
    # Exam URLs
    path('', views.ExamListCreateView.as_view(), name='exam-list-create'),
    path('<int:pk>/', views.ExamDetailView.as_view(), name='exam-detail'),

    # Question Bank URLs
    path('questions/', views.QuestionBankListCreateView.as_view(), name='question-bank-list-create'),
    path('questions/<int:pk>/', views.QuestionBankDetailView.as_view(), name='question-bank-detail'),

    # Student Exam URLs
    path('student-exams/', views.StudentExamListView.as_view(), name='student-exam-list'),
    path('register/', views.ExamRegistrationView.as_view(), name='exam-registration'),

    # Results URLs
    path('results/', views.ExamResultListView.as_view(), name='exam-result-list'),
    path('results/<int:pk>/', views.ExamResultDetailView.as_view(), name='exam-result-detail'),
]
