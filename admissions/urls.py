from django.urls import path
from . import views

urlpatterns = [
    # Root API endpoint
    path('', views.admissions_api_root, name='admissions-api-root'),

    # Admission Cycle URLs
    path('cycles/', views.AdmissionCycleListView.as_view(), name='admission-cycle-list'),

    # Applicant URLs
    path('applicants/', views.ApplicantListCreateView.as_view(), name='applicant-list-create'),
    path('applicants/<int:pk>/', views.ApplicantDetailView.as_view(), name='applicant-detail'),

    # Application URLs
    path('applications/', views.ApplicationListCreateView.as_view(), name='application-list-create'),

    # Admission Decision Management URLs
    path('applications/<int:application_id>/admit/', views.admit_applicant, name='admit-applicant'),
    path('applications/<int:application_id>/reject/', views.reject_applicant, name='reject-applicant'),
    path('applications/<int:application_id>/status/', views.check_admission_status, name='check-admission-status'),

    # Fee Payment URLs
    path('applications/<int:application_id>/pay-fee/', views.record_fee_payment, name='record-fee-payment'),

    # PDF Generation URLs
    path('applications/<int:application_id>/admission-letter/', views.generate_admission_letter, name='generate-admission-letter'),

    # Document URLs
    path('documents/', views.DocumentUploadView.as_view(), name='document-upload'),

    # Test URLs
    path('tests/', views.AdmissionTestListView.as_view(), name='admission-test-list'),
    path('test-results/', views.TestResultListView.as_view(), name='test-result-list'),

    # Applicant Portal URLs
    path('portal/<str:application_number>/', views.applicant_portal_status, name='applicant-portal-status'),
]
