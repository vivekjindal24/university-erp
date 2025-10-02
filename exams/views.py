from rest_framework import generics, permissions
from .models import (
    ExamType, Exam, QuestionBank, ExamQuestion, StudentExam,
    ExamResult, AnswerSheet, QuestionAnswer, GradingRubric
)

class ExamListCreateView(generics.ListCreateAPIView):
    queryset = Exam.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class ExamSerializer(serializers.ModelSerializer):
            class Meta:
                model = Exam
                fields = '__all__'
        return ExamSerializer

class ExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class ExamSerializer(serializers.ModelSerializer):
            class Meta:
                model = Exam
                fields = '__all__'
        return ExamSerializer

class QuestionBankListCreateView(generics.ListCreateAPIView):
    queryset = QuestionBank.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class QuestionBankSerializer(serializers.ModelSerializer):
            class Meta:
                model = QuestionBank
                fields = '__all__'
        return QuestionBankSerializer

class QuestionBankDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuestionBank.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class QuestionBankSerializer(serializers.ModelSerializer):
            class Meta:
                model = QuestionBank
                fields = '__all__'
        return QuestionBankSerializer

class StudentExamListView(generics.ListAPIView):
    queryset = StudentExam.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class StudentExamSerializer(serializers.ModelSerializer):
            class Meta:
                model = StudentExam
                fields = '__all__'
        return StudentExamSerializer

class ExamRegistrationView(generics.CreateAPIView):
    queryset = StudentExam.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class StudentExamSerializer(serializers.ModelSerializer):
            class Meta:
                model = StudentExam
                fields = '__all__'
        return StudentExamSerializer

class ExamResultListView(generics.ListAPIView):
    queryset = ExamResult.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class ExamResultSerializer(serializers.ModelSerializer):
            class Meta:
                model = ExamResult
                fields = '__all__'
        return ExamResultSerializer

class ExamResultDetailView(generics.RetrieveUpdateAPIView):
    queryset = ExamResult.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class ExamResultSerializer(serializers.ModelSerializer):
            class Meta:
                model = ExamResult
                fields = '__all__'
        return ExamResultSerializer
