from django.urls import path
from . import views

urlpatterns = [
    # Announcement URLs
    path('announcements/', views.AnnouncementListCreateView.as_view(), name='announcement-list-create'),
    path('announcements/<int:pk>/', views.AnnouncementDetailView.as_view(), name='announcement-detail'),

    # Committee URLs
    path('committees/', views.CommitteeListView.as_view(), name='committee-list'),
    path('meetings/', views.MeetingListCreateView.as_view(), name='meeting-list-create'),

    # Policy URLs
    path('policies/', views.PolicyListView.as_view(), name='policy-list'),

    # Grievance URLs
    path('grievances/', views.GrievanceListCreateView.as_view(), name='grievance-list-create'),
    path('grievances/<int:pk>/', views.GrievanceDetailView.as_view(), name='grievance-detail'),

    # Report URLs
    path('reports/', views.ReportListCreateView.as_view(), name='report-list-create'),
    path('reports/<int:pk>/download/', views.ReportDownloadView.as_view(), name='report-download'),
]
