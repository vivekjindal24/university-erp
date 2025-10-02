from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import (
    AdmissionCycle, AdmissionRequirement, Applicant, Application,
    ApplicationDocument, AdmissionTest, TestRegistration, TestResult, AdmissionFee
)
from .pdf_utils import generate_admission_letter_pdf, generate_fee_receipt_pdf
from .email_utils import send_admission_confirmation_email, send_rejection_email, send_fee_payment_confirmation_email

@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Allow unauthenticated access to API root
def admissions_api_root(request):
    """
    Root API view for admissions module showing available endpoints
    """
    return Response({
        'message': 'Welcome to the University ERP Admissions API',
        'status': 'Server is running successfully',
        'authentication_note': 'Some endpoints require authentication. For testing, you can use the admin credentials.',
        'public_endpoints': {
            'portal_status': '/api/admissions/portal/{application_number}/ - Check applicant portal status (No auth required)',
            'cycles': '/api/admissions/cycles/ - List admission cycles (No auth required)',
            'applications': '/api/admissions/applications/ - List applications (No auth required)',
        },
        'protected_endpoints': {
            'admit_student': '/api/admissions/applications/{id}/admit/ - Admit an applicant (Auth required)',
            'reject_student': '/api/admissions/applications/{id}/reject/ - Reject an applicant (Auth required)',
            'record_payment': '/api/admissions/applications/{id}/pay-fee/ - Record fee payment (Auth required)',
            'download_letter': '/api/admissions/applications/{id}/admission-letter/ - Download admission letter (Auth required)',
        },
        'test_endpoints': {
            'check_kunal_status': '/api/admissions/portal/APP2025003/ - Check Kunal Tomar\'s admission status',
            'list_applications': '/api/admissions/applications/ - See all applications',
            'list_cycles': '/api/admissions/cycles/ - See admission cycles',
        },
        'authentication_help': {
            'admin_login': 'Use admin/admin123 credentials for authenticated endpoints',
            'token_auth': 'The system uses JWT token authentication for API access'
        }
    })

class AdmissionCycleListView(generics.ListAPIView):
    queryset = AdmissionCycle.objects.all()
    permission_classes = [permissions.AllowAny]  # Allow public access

    def get_serializer_class(self):
        from rest_framework import serializers
        class AdmissionCycleSerializer(serializers.ModelSerializer):
            class Meta:
                model = AdmissionCycle
                fields = '__all__'
        return AdmissionCycleSerializer

class ApplicantListCreateView(generics.ListCreateAPIView):
    queryset = Applicant.objects.all()
    permission_classes = [permissions.AllowAny]  # Allow public access for viewing

    def get_serializer_class(self):
        from rest_framework import serializers
        class ApplicantSerializer(serializers.ModelSerializer):
            class Meta:
                model = Applicant
                fields = '__all__'
        return ApplicantSerializer

class ApplicantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Applicant.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Read access for all, write for authenticated

    def get_serializer_class(self):
        from rest_framework import serializers
        class ApplicantSerializer(serializers.ModelSerializer):
            class Meta:
                model = Applicant
                fields = '__all__'
        return ApplicantSerializer

class ApplicationListCreateView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    permission_classes = [permissions.AllowAny]  # Allow public access for viewing

    def get_serializer_class(self):
        from rest_framework import serializers
        class ApplicationSerializer(serializers.ModelSerializer):
            applicant_name = serializers.SerializerMethodField()
            program_name = serializers.SerializerMethodField()
            admission_cycle_name = serializers.SerializerMethodField()
            fee_payment_status = serializers.SerializerMethodField()

            class Meta:
                model = Application
                fields = '__all__'

            def get_applicant_name(self, obj):
                return f"{obj.applicant.first_name} {obj.applicant.last_name}"

            def get_program_name(self, obj):
                return obj.program.name

            def get_admission_cycle_name(self, obj):
                return obj.admission_cycle.name

            def get_fee_payment_status(self, obj):
                return {
                    'first_semester_fee_paid': obj.first_semester_fee_paid,
                    'first_semester_fee_amount': obj.first_semester_fee_amount,
                    'first_semester_fee_payment_date': obj.first_semester_fee_payment_date
                }
        return ApplicationSerializer

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def admit_applicant(request, application_id):
    """
    Mark an applicant as admitted and set first semester fee
    """
    try:
        application = get_object_or_404(Application, id=application_id)

        # Get fee amount from request
        fee_amount = request.data.get('first_semester_fee_amount')
        if not fee_amount:
            return Response(
                {'error': 'First semester fee amount is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update application status
        application.admission_decision = 'admitted'
        application.status = 'admitted'
        application.admission_decision_date = timezone.now()
        application.admission_decision_by = request.user
        application.first_semester_fee_amount = fee_amount
        application.save()

        # Send admission confirmation email
        email_sent = send_admission_confirmation_email(application)

        return Response({
            'message': 'Applicant admitted successfully',
            'application_id': application.id,
            'admission_decision': application.admission_decision,
            'first_semester_fee_amount': application.first_semester_fee_amount,
            'email_sent': email_sent
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reject_applicant(request, application_id):
    """
    Mark an applicant as not admitted
    """
    try:
        application = get_object_or_404(Application, id=application_id)

        # Update application status
        application.admission_decision = 'not_admitted'
        application.status = 'rejected'
        application.admission_decision_date = timezone.now()
        application.admission_decision_by = request.user
        application.save()

        # Send rejection email
        email_sent = send_rejection_email(application)

        return Response({
            'message': 'Applicant rejected successfully',
            'application_id': application.id,
            'admission_decision': application.admission_decision,
            'email_sent': email_sent
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def record_fee_payment(request, application_id):
    """
    Record first semester fee payment for an admitted student
    """
    try:
        application = get_object_or_404(Application, id=application_id)

        if application.admission_decision != 'admitted':
            return Response(
                {'error': 'Only admitted students can pay fees'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get payment details from request
        payment_amount = request.data.get('payment_amount')
        transaction_id = request.data.get('transaction_id', '')
        payment_method = request.data.get('payment_method', 'Online')

        if not payment_amount:
            return Response(
                {'error': 'Payment amount is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update payment status
        application.first_semester_fee_paid = True
        application.first_semester_fee_payment_date = timezone.now()
        application.first_semester_fee_transaction_id = transaction_id
        application.save()

        # Create fee record
        AdmissionFee.objects.create(
            application=application,
            fee_type='tuition_fee',
            amount=payment_amount,
            paid_amount=payment_amount,
            payment_date=timezone.now(),
            payment_method=payment_method,
            transaction_id=transaction_id,
            is_paid=True,
            due_date=timezone.now().date()
        )

        # Send fee payment confirmation email
        payment_details = {
            'amount': float(payment_amount),
            'transaction_id': transaction_id,
            'payment_method': payment_method,
            'payment_date': application.first_semester_fee_payment_date
        }
        email_sent = send_fee_payment_confirmation_email(application, payment_details)

        return Response({
            'message': 'Fee payment recorded successfully',
            'application_id': application.id,
            'fee_paid': application.first_semester_fee_paid,
            'payment_date': application.first_semester_fee_payment_date,
            'transaction_id': transaction_id,
            'email_sent': email_sent
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Allow public access for status checking
def check_admission_status(request, application_id):
    """
    Check admission status and fee payment status for an application
    """
    try:
        application = get_object_or_404(Application, id=application_id)

        return Response({
            'application_id': application.id,
            'applicant_name': f"{application.applicant.first_name} {application.applicant.last_name}",
            'application_number': application.applicant.application_number,
            'program_name': application.program.name,
            'admission_decision': application.admission_decision,
            'admission_decision_date': application.admission_decision_date,
            'first_semester_fee_amount': application.first_semester_fee_amount,
            'first_semester_fee_paid': application.first_semester_fee_paid,
            'first_semester_fee_payment_date': application.first_semester_fee_payment_date,
            'admission_letter_generated': application.admission_letter_generated,
            'can_generate_letter': application.admission_decision == 'admitted'
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])  # Keep PDF generation protected
def generate_admission_letter(request, application_id):
    """
    Generate and download provisional admission letter PDF
    """
    try:
        application = get_object_or_404(Application, id=application_id)

        if application.admission_decision != 'admitted':
            return Response(
                {'error': 'Admission letter can only be generated for admitted students'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate PDF
        pdf_buffer = generate_admission_letter_pdf(application)

        # Update letter generation status
        application.admission_letter_generated = True
        application.admission_letter_generated_date = timezone.now()
        application.save()

        # Create HTTP response
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="admission_letter_{application.applicant.application_number}.pdf"'

        return response

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Allow public access to portal status
def applicant_portal_status(request, application_number):
    """
    Get application status for applicant portal
    """
    try:
        applicant = get_object_or_404(Applicant, application_number=application_number)
        applications = Application.objects.filter(applicant=applicant).select_related('program', 'admission_cycle')

        application_data = []
        for app in applications:
            app_data = {
                'id': app.id,
                'program_name': app.program.name,
                'admission_cycle': app.admission_cycle.name,
                'application_status': app.status,
                'admission_decision': app.admission_decision,
                'admission_decision_date': app.admission_decision_date,
                'first_semester_fee_amount': app.first_semester_fee_amount,
                'first_semester_fee_paid': app.first_semester_fee_paid,
                'first_semester_fee_payment_date': app.first_semester_fee_payment_date,
                'admission_letter_generated': app.admission_letter_generated,
                'can_download_letter': app.admission_decision == 'admitted' and app.admission_letter_generated
            }
            application_data.append(app_data)

        return Response({
            'applicant_name': f"{applicant.first_name} {applicant.last_name}",
            'application_number': applicant.application_number,
            'email': applicant.email,
            'applications': application_data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class DocumentUploadView(generics.ListCreateAPIView):
    queryset = ApplicationDocument.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Read access for all

    def get_serializer_class(self):
        from rest_framework import serializers
        class DocumentSerializer(serializers.ModelSerializer):
            class Meta:
                model = ApplicationDocument
                fields = '__all__'
        return DocumentSerializer

class AdmissionTestListView(generics.ListAPIView):
    queryset = AdmissionTest.objects.all()
    permission_classes = [permissions.AllowAny]  # Allow public access

    def get_serializer_class(self):
        from rest_framework import serializers
        class AdmissionTestSerializer(serializers.ModelSerializer):
            class Meta:
                model = AdmissionTest
                fields = '__all__'
        return AdmissionTestSerializer

class TestResultListView(generics.ListAPIView):
    queryset = TestResult.objects.all()
    permission_classes = [permissions.AllowAny]  # Allow public access

    def get_serializer_class(self):
        from rest_framework import serializers
        class TestResultSerializer(serializers.ModelSerializer):
            class Meta:
                model = TestResult
                fields = '__all__'
        return TestResultSerializer
