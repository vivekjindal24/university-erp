from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import (
    Announcement, Committee, CommitteeMember, Meeting, MeetingAttendance,
    Policy, Grievance, Report, AuditLog
)

class AnnouncementListCreateView(generics.ListCreateAPIView):
    queryset = Announcement.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class AnnouncementSerializer(serializers.ModelSerializer):
            class Meta:
                model = Announcement
                fields = '__all__'
        return AnnouncementSerializer

class AnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Announcement.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class AnnouncementSerializer(serializers.ModelSerializer):
            class Meta:
                model = Announcement
                fields = '__all__'
        return AnnouncementSerializer

class CommitteeListView(generics.ListAPIView):
    queryset = Committee.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class CommitteeSerializer(serializers.ModelSerializer):
            class Meta:
                model = Committee
                fields = '__all__'
        return CommitteeSerializer

class MeetingListCreateView(generics.ListCreateAPIView):
    queryset = Meeting.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class MeetingSerializer(serializers.ModelSerializer):
            class Meta:
                model = Meeting
                fields = '__all__'
        return MeetingSerializer

class PolicyListView(generics.ListAPIView):
    queryset = Policy.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class PolicySerializer(serializers.ModelSerializer):
            class Meta:
                model = Policy
                fields = '__all__'
        return PolicySerializer

class GrievanceListCreateView(generics.ListCreateAPIView):
    queryset = Grievance.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class GrievanceSerializer(serializers.ModelSerializer):
            class Meta:
                model = Grievance
                fields = '__all__'
        return GrievanceSerializer

class GrievanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grievance.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class GrievanceSerializer(serializers.ModelSerializer):
            class Meta:
                model = Grievance
                fields = '__all__'
        return GrievanceSerializer

class ReportListCreateView(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class ReportSerializer(serializers.ModelSerializer):
            class Meta:
                model = Report
                fields = '__all__'
        return ReportSerializer

class ReportDownloadView(generics.RetrieveAPIView):
    queryset = Report.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response({'download_url': f'/media/reports/{instance.file_path}'})
