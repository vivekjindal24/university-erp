from rest_framework import generics, permissions
from .models import (
    Faculty, CourseAssignment, FacultyLeave, FacultyEvaluation,
    ResearchWork, FacultyWorkload
)
from .serializers import (
    FacultySerializer, CourseAssignmentSerializer, FacultyLeaveSerializer,
    FacultyEvaluationSerializer, ResearchWorkSerializer, FacultyWorkloadSerializer
)

class FacultyListCreateView(generics.ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [permissions.IsAuthenticated]

class FacultyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [permissions.IsAuthenticated]

class CourseAssignmentListView(generics.ListAPIView):
    queryset = CourseAssignment.objects.all()
    serializer_class = CourseAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class CourseAssignmentCreateView(generics.CreateAPIView):
    queryset = CourseAssignment.objects.all()
    serializer_class = CourseAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class FacultyLeaveListCreateView(generics.ListCreateAPIView):
    queryset = FacultyLeave.objects.all()
    serializer_class = FacultyLeaveSerializer
    permission_classes = [permissions.IsAuthenticated]

class FacultyLeaveDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacultyLeave.objects.all()
    serializer_class = FacultyLeaveSerializer
    permission_classes = [permissions.IsAuthenticated]

class FacultyEvaluationListView(generics.ListAPIView):
    queryset = FacultyEvaluation.objects.all()
    serializer_class = FacultyEvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

class ResearchWorkListCreateView(generics.ListCreateAPIView):
    queryset = ResearchWork.objects.all()
    serializer_class = ResearchWorkSerializer
    permission_classes = [permissions.IsAuthenticated]
