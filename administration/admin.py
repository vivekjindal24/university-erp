from django.contrib import admin
from .models import (
    Announcement, Committee, CommitteeMember, Meeting, MeetingAttendance,
    Policy, Grievance, Report, AuditLog
)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'announcement_type', 'target_audience', 'priority', 'is_active', 'publish_date')
    list_filter = ('announcement_type', 'target_audience', 'priority', 'is_active', 'publish_date')
    search_fields = ('title', 'content')
    date_hierarchy = 'publish_date'

@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ('name', 'committee_type', 'chairperson', 'establishment_date', 'is_active')
    list_filter = ('committee_type', 'is_active', 'establishment_date')
    search_fields = ('name', 'description')

@admin.register(CommitteeMember)
class CommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ('committee', 'user', 'role', 'start_date', 'end_date', 'is_active')
    list_filter = ('role', 'is_active', 'committee__committee_type')
    search_fields = ('committee__name', 'user__first_name', 'user__last_name')

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'committee', 'meeting_date', 'duration_minutes', 'status', 'created_by')
    list_filter = ('status', 'committee', 'meeting_date')
    search_fields = ('title', 'committee__name', 'agenda')
    date_hierarchy = 'meeting_date'

@admin.register(MeetingAttendance)
class MeetingAttendanceAdmin(admin.ModelAdmin):
    list_display = ('meeting', 'member', 'status', 'arrival_time', 'departure_time')
    list_filter = ('status', 'meeting__committee')
    search_fields = ('meeting__title', 'member__user__first_name', 'member__user__last_name')

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('policy_number', 'title', 'policy_type', 'status', 'effective_date', 'review_date')
    list_filter = ('policy_type', 'status', 'effective_date')
    search_fields = ('policy_number', 'title', 'description')

@admin.register(Grievance)
class GrievanceAdmin(admin.ModelAdmin):
    list_display = ('grievance_id', 'complainant', 'grievance_type', 'priority', 'status', 'assigned_to')
    list_filter = ('grievance_type', 'priority', 'status', 'is_anonymous')
    search_fields = ('grievance_id', 'subject', 'description')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'status', 'generated_by', 'generated_at', 'download_count')
    list_filter = ('report_type', 'status', 'is_scheduled', 'generated_at')
    search_fields = ('title', 'description')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'model_name', 'object_repr', 'timestamp', 'ip_address')
    list_filter = ('action_type', 'model_name', 'timestamp')
    search_fields = ('user__username', 'model_name', 'object_repr')
    readonly_fields = ('user', 'action_type', 'model_name', 'object_id', 'object_repr', 'changes', 'ip_address', 'user_agent', 'timestamp', 'session_key')
    date_hierarchy = 'timestamp'
