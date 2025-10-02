from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from .models import (
    AdmissionCycle, AdmissionRequirement, Applicant, Application,
    ApplicationDocument, AdmissionTest, TestRegistration, TestResult, AdmissionFee
)
from .email_utils import send_admission_confirmation_email, send_rejection_email, send_fee_payment_confirmation_email

@admin.register(AdmissionCycle)
class AdmissionCycleAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year', 'application_start_date', 'application_end_date', 'is_active')
    list_filter = ('is_active', 'academic_year')
    search_fields = ('name', 'academic_year')
    date_hierarchy = 'application_start_date'

@admin.register(AdmissionRequirement)
class AdmissionRequirementAdmin(admin.ModelAdmin):
    list_display = ('program', 'admission_cycle', 'minimum_percentage', 'total_seats', 'application_fee')
    list_filter = ('program__department', 'admission_cycle')
    search_fields = ('program__name', 'admission_cycle__name')

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('application_number', 'first_name', 'last_name', 'email', 'phone_number', 'category')
    list_filter = ('gender', 'category', 'nationality', 'created_at')
    search_fields = ('application_number', 'first_name', 'last_name', 'email', 'phone_number')
    date_hierarchy = 'created_at'

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'applicant',
        'program',
        'admission_cycle',
        'status',
        'admission_decision_status',
        'fee_payment_status',
        'application_fee_paid',
        'merit_rank',
        'admission_actions'
    )
    list_filter = (
        'status',
        'admission_decision',
        'first_semester_fee_paid',
        'program',
        'admission_cycle',
        'application_fee_paid'
    )
    search_fields = ('applicant__application_number', 'applicant__first_name', 'applicant__last_name')
    readonly_fields = (
        'application_date',
        'created_at',
        'updated_at',
        'admission_decision_date',
        'admission_letter_generated_date',
        'first_semester_fee_payment_date'
    )

    fieldsets = (
        ('Application Information', {
            'fields': ('applicant', 'program', 'admission_cycle', 'status')
        }),
        ('Academic Details', {
            'fields': (
                'previous_school_name', 'previous_school_board',
                'graduation_year', 'overall_percentage'
            )
        }),
        ('Test & Interview', {
            'fields': (
                'entrance_exam_score', 'entrance_exam_rank',
                'interview_date', 'interview_score', 'interview_feedback'
            )
        }),
        ('Selection Details', {
            'fields': ('merit_score', 'merit_rank', 'waitlist_number')
        }),
        ('Admission Decision', {
            'fields': (
                'admission_decision', 'admission_decision_date',
                'admission_decision_by', 'admission_letter_generated',
                'admission_letter_generated_date'
            )
        }),
        ('Fee Information', {
            'fields': (
                'first_semester_fee_amount', 'first_semester_fee_paid',
                'first_semester_fee_payment_date', 'first_semester_fee_transaction_id'
            )
        }),
        ('Application Fees', {
            'fields': ('application_fee_paid', 'application_fee_amount', 'payment_reference')
        }),
        ('Review Information', {
            'fields': ('reviewed_by', 'review_date', 'review_comments')
        }),
        ('Additional Information', {
            'fields': ('statement_of_purpose', 'extracurricular_activities', 'work_experience')
        }),
        ('Timestamps', {
            'fields': ('application_date', 'submission_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def admission_decision_status(self, obj):
        """Display admission decision with color coding"""
        if obj.admission_decision == 'admitted':
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ ADMITTED</span>'
            )
        elif obj.admission_decision == 'not_admitted':
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ NOT ADMITTED</span>'
            )
        else:
            return format_html(
                '<span style="color: orange; font-weight: bold;">⏳ PENDING</span>'
            )
    admission_decision_status.short_description = 'Admission Status'

    def fee_payment_status(self, obj):
        """Display fee payment status with color coding"""
        if obj.admission_decision == 'admitted':
            try:
                amount = obj.first_semester_fee_amount
                if amount is None:
                    amount = Decimal('0')
                elif not isinstance(amount, Decimal):
                    amount = Decimal(str(amount))
            except (InvalidOperation, ValueError, TypeError):
                amount = Decimal('0')
            formatted_amount = f"₹{amount:,.2f}"

            if obj.first_semester_fee_paid:
                return format_html(
                    '<span style="color: green; font-weight: bold;">✓ PAID ({})</span>',
                    formatted_amount
                )
            else:
                return format_html(
                    '<span style="color: red; font-weight: bold;">✗ PENDING ({})</span>',
                    formatted_amount
                )
        else:
            return format_html('<span style="color: gray;">N/A</span>')
    fee_payment_status.short_description = 'Fee Status'

    def admission_actions(self, obj):
        """Display action buttons for admission management"""
        actions = []

        if obj.admission_decision == 'pending':
            # Admit button
            admit_url = reverse('admin:admit_applicant', args=[obj.id])
            actions.append(
                f'<a href="{admit_url}" class="button" style="background-color: #28a745; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px; margin-right: 5px;">Admit</a>'
            )

            # Reject button
            reject_url = reverse('admin:reject_applicant', args=[obj.id])
            actions.append(
                f'<a href="{reject_url}" class="button" style="background-color: #dc3545; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px; margin-right: 5px;">Reject</a>'
            )

        elif obj.admission_decision == 'admitted':
            # Generate admission letter button
            letter_url = reverse('admin:generate_admission_letter', args=[obj.id])
            actions.append(
                f'<a href="{letter_url}" target="_blank" class="button" style="background-color: #007bff; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px; margin-right: 5px;">Download Letter</a>'
            )

            # Record fee payment button (if not paid)
            if not obj.first_semester_fee_paid:
                fee_url = reverse('admin:record_fee_payment', args=[obj.id])
                actions.append(
                    f'<a href="{fee_url}" class="button" style="background-color: #ffc107; color: black; padding: 5px 10px; text-decoration: none; border-radius: 3px; margin-right: 5px;">Record Payment</a>'
                )

        return mark_safe(''.join(actions)) if actions else '-'
    admission_actions.short_description = 'Actions'

    def get_urls(self):
        """Add custom URLs for admission actions"""
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                'admit/<int:application_id>/',
                self.admin_site.admin_view(self.admit_applicant_view),
                name='admit_applicant',
            ),
            path(
                'reject/<int:application_id>/',
                self.admin_site.admin_view(self.reject_applicant_view),
                name='reject_applicant',
            ),
            path(
                'generate-letter/<int:application_id>/',
                self.admin_site.admin_view(self.generate_letter_view),
                name='generate_admission_letter',
            ),
            path(
                'record-payment/<int:application_id>/',
                self.admin_site.admin_view(self.record_payment_view),
                name='record_fee_payment',
            ),
        ]
        return custom_urls + urls

    def admit_applicant_view(self, request, application_id):
        """Custom view to admit an applicant"""
        application = Application.objects.get(id=application_id)

        if request.method == 'POST':
            fee_amount = request.POST.get('fee_amount')
            if fee_amount:
                try:
                    application.admission_decision = 'admitted'
                    application.status = 'admitted'
                    application.admission_decision_date = timezone.now()
                    application.admission_decision_by = request.user
                    application.first_semester_fee_amount = Decimal(str(fee_amount))
                    application.save()
                except (InvalidOperation, ValueError, TypeError):
                    messages.error(request, 'Invalid fee amount. Please enter a valid number.')
                    return HttpResponseRedirect(reverse('admin:admissions_application_changelist'))

                # Send admission confirmation email
                email_sent = send_admission_confirmation_email(application)

                if email_sent:
                    messages.success(request, f'Applicant {application.applicant.first_name} {application.applicant.last_name} has been admitted successfully! Confirmation email sent to {application.applicant.email}.')
                else:
                    messages.success(request, f'Applicant {application.applicant.first_name} {application.applicant.last_name} has been admitted successfully!')
                    messages.warning(request, 'Admission email could not be sent. Please check email configuration.')
            else:
                messages.error(request, 'Please provide the first semester fee amount.')
        else:
            # Render a simple form for fee amount input
            from django.template.response import TemplateResponse
            context = {
                'application': application,
                'title': f'Admit Applicant - {application.applicant.first_name} {application.applicant.last_name}',
            }
            return TemplateResponse(request, 'admin/admissions/admit_form.html', context)

        return HttpResponseRedirect(reverse('admin:admissions_application_changelist'))

    def reject_applicant_view(self, request, application_id):
        """Custom view to reject an applicant"""
        application = Application.objects.get(id=application_id)

        application.admission_decision = 'not_admitted'
        application.status = 'rejected'
        application.admission_decision_date = timezone.now()
        application.admission_decision_by = request.user
        application.save()

        # Send rejection email
        email_sent = send_rejection_email(application)

        if email_sent:
            messages.success(request, f'Applicant {application.applicant.first_name} {application.applicant.last_name} has been rejected. Notification email sent to {application.applicant.email}.')
        else:
            messages.success(request, f'Applicant {application.applicant.first_name} {application.applicant.last_name} has been rejected.')
            messages.warning(request, 'Rejection email could not be sent. Please check email configuration.')

        return HttpResponseRedirect(reverse('admin:admissions_application_changelist'))

    def generate_letter_view(self, request, application_id):
        """Custom view to generate admission letter"""
        from .pdf_utils import generate_admission_letter_pdf
        from django.http import HttpResponse

        application = Application.objects.get(id=application_id)

        if application.admission_decision != 'admitted':
            messages.error(request, 'Admission letter can only be generated for admitted students.')
            return HttpResponseRedirect(reverse('admin:admissions_application_changelist'))

        # Generate PDF
        pdf_buffer = generate_admission_letter_pdf(application)

        # Update letter generation status
        application.admission_letter_generated = True
        application.admission_letter_generated_date = timezone.now()
        application.save()

        # Return PDF response
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="admission_letter_{application.applicant.application_number}.pdf"'

        return response

    def record_payment_view(self, request, application_id):
        """Custom view to record fee payment"""
        application = Application.objects.get(id=application_id)

        if request.method == 'POST':
            payment_amount = request.POST.get('payment_amount')
            transaction_id = request.POST.get('transaction_id', '')
            payment_method = request.POST.get('payment_method', 'Online')

            if payment_amount:
                try:
                    application.first_semester_fee_paid = True
                    application.first_semester_fee_payment_date = timezone.now()
                    application.first_semester_fee_transaction_id = transaction_id
                    application.save()

                    # Create fee record
                    AdmissionFee.objects.create(
                        application=application,
                        fee_type='tuition_fee',
                        amount=Decimal(str(payment_amount)),
                        paid_amount=Decimal(str(payment_amount)),
                        payment_date=timezone.now(),
                        payment_method=payment_method,
                        transaction_id=transaction_id,
                        is_paid=True,
                        due_date=timezone.now().date()
                    )
                except (InvalidOperation, ValueError, TypeError):
                    messages.error(request, 'Invalid payment amount. Please enter a valid number.')
                    return HttpResponseRedirect(reverse('admin:admissions_application_changelist'))

                # Send fee payment confirmation email
                payment_details = {
                    'amount': float(payment_amount),
                    'transaction_id': transaction_id,
                    'payment_method': payment_method,
                    'payment_date': application.first_semester_fee_payment_date
                }
                email_sent = send_fee_payment_confirmation_email(application, payment_details)

                if email_sent:
                    messages.success(request, f'Fee payment of ₹{payment_amount} recorded successfully! Confirmation email sent to {application.applicant.email}.')
                else:
                    messages.success(request, f'Fee payment of ₹{payment_amount} recorded successfully!')
                    messages.warning(request, 'Payment confirmation email could not be sent. Please check email configuration.')
            else:
                messages.error(request, 'Please provide the payment amount.')
        else:
            # Render a simple form for payment details
            from django.template.response import TemplateResponse
            context = {
                'application': application,
                'title': f'Record Fee Payment - {application.applicant.first_name} {application.applicant.last_name}',
            }
            return TemplateResponse(request, 'admin/admissions/payment_form.html', context)

        return HttpResponseRedirect(reverse('admin:admissions_application_changelist'))

@admin.register(ApplicationDocument)
class ApplicationDocumentAdmin(admin.ModelAdmin):
    list_display = ('application', 'document_type', 'verification_status', 'is_mandatory', 'uploaded_at')
    list_filter = ('document_type', 'verification_status', 'is_mandatory')
    search_fields = ('application__applicant__application_number', 'document_name')

@admin.register(AdmissionTest)
class AdmissionTestAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'program', 'test_type', 'test_date', 'total_marks', 'is_active')
    list_filter = ('test_type', 'program', 'is_active')
    search_fields = ('test_name', 'program__name')
    date_hierarchy = 'test_date'

@admin.register(TestRegistration)
class TestRegistrationAdmin(admin.ModelAdmin):
    list_display = ('application', 'test', 'admit_card_number', 'seat_number', 'is_appeared')
    list_filter = ('test', 'is_appeared')
    search_fields = ('application__applicant__application_number', 'admit_card_number')

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('test_registration', 'marks_obtained', 'percentage', 'rank', 'grade')
    list_filter = ('test_registration__test', 'grade')
    search_fields = ('test_registration__application__applicant__application_number',)

@admin.register(AdmissionFee)
class AdmissionFeeAdmin(admin.ModelAdmin):
    list_display = ('application', 'fee_type', 'amount', 'paid_amount', 'is_paid', 'payment_date')
    list_filter = ('fee_type', 'is_paid', 'payment_method')
    search_fields = ('application__applicant__application_number', 'transaction_id')
    date_hierarchy = 'payment_date'
