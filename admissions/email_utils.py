"""
Email utilities for admission notifications
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

def send_admission_confirmation_email(application):
    """
    Send admission confirmation email to the admitted student
    """
    try:
        applicant = application.applicant

        # Email subject
        subject = f'Admission Confirmation - {application.program.name}'

        # Email context
        context = {
            'applicant_name': f"{applicant.first_name} {applicant.last_name}",
            'application_number': applicant.application_number,
            'program_name': application.program.name,
            'department_name': getattr(application.program.department, 'name', 'University'),
            'academic_year': application.admission_cycle.academic_year,
            'admission_cycle': application.admission_cycle.name,
            'first_semester_fee': application.first_semester_fee_amount or Decimal('0'),
            'admission_date': application.admission_decision_date,
            'session_start_date': application.admission_cycle.session_start_date,
            'confirmation_deadline': application.admission_cycle.admission_confirmation_deadline,
        }

        # Create email content
        email_content = f"""
Dear {context['applicant_name']},

Congratulations! We are delighted to inform you that you have been ADMITTED to the {context['program_name']} program for the academic year {context['academic_year']}.

ADMISSION DETAILS:
• Application Number: {context['application_number']}
• Program: {context['program_name']}
• Academic Year: {context['academic_year']}
• Admission Date: {context['admission_date'].strftime('%B %d, %Y') if context['admission_date'] else 'N/A'}

FIRST SEMESTER FEE:
• Amount: ₹{context['first_semester_fee']:,.2f}
• Payment Status: {'PAID' if application.first_semester_fee_paid else 'PENDING'}

IMPORTANT NEXT STEPS:
1. Download your provisional admission letter from the student portal
2. Pay the first semester fee to confirm your admission
3. Submit all required original documents for verification
4. Complete the admission formalities before the deadline

IMPORTANT DATES:
• Session Start Date: {context['session_start_date']}
• Confirmation Deadline: {context['confirmation_deadline'] or 'To be announced'}

CONTACT INFORMATION:
For any queries regarding your admission, please contact:
• Admission Office: admissions@university.edu
• Phone: +1-234-567-8900
• Office Hours: Monday to Friday, 9:00 AM to 5:00 PM

We look forward to welcoming you to our university community!

Best regards,
Admission Office
University ERP System

---
This is an automated email. Please do not reply to this email address.
"""

        # Send email
        send_mail(
            subject=subject,
            message=email_content,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'admissions@university.edu'),
            recipient_list=[applicant.email],
            fail_silently=False,
        )

        logger.info(f"Admission confirmation email sent to {applicant.email} for application {applicant.application_number}")
        return True

    except Exception as e:
        logger.error(f"Failed to send admission confirmation email: {str(e)}")
        return False

def send_rejection_email(application):
    """
    Send admission rejection email to the applicant
    """
    try:
        applicant = application.applicant

        # Email subject
        subject = f'Admission Decision - {application.program.name}'

        # Email content
        email_content = f"""
Dear {applicant.first_name} {applicant.last_name},

Thank you for your interest in the {application.program.name} program at our university for the academic year {application.admission_cycle.academic_year}.

After careful consideration of your application (Application Number: {applicant.application_number}), we regret to inform you that we are unable to offer you admission to this program at this time.

We received a large number of highly qualified applications this year, making the selection process extremely competitive. Please know that this decision does not reflect on your abilities or potential for success.

We encourage you to:
• Consider applying to other programs that might be a good fit
• Apply again in future admission cycles
• Contact our admission office if you have any questions

We wish you all the best in your academic endeavors.

Best regards,
Admission Office
University ERP System

---
This is an automated email. Please do not reply to this email address.
"""

        # Send email
        send_mail(
            subject=subject,
            message=email_content,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'admissions@university.edu'),
            recipient_list=[applicant.email],
            fail_silently=False,
        )

        logger.info(f"Admission rejection email sent to {applicant.email} for application {applicant.application_number}")
        return True

    except Exception as e:
        logger.error(f"Failed to send admission rejection email: {str(e)}")
        return False

def send_fee_payment_confirmation_email(application, payment_details):
    """
    Send fee payment confirmation email to the student
    """
    try:
        applicant = application.applicant

        # Email subject
        subject = f'Fee Payment Confirmation - {application.program.name}'

        # Email content
        payment_amount = payment_details.get('amount', application.first_semester_fee_amount) or Decimal('0')
        try:
            payment_amount = Decimal(str(payment_amount))
        except Exception:
            payment_amount = Decimal('0')
        transaction_id = payment_details.get('transaction_id', application.first_semester_fee_transaction_id)
        payment_date = payment_details.get('payment_date', application.first_semester_fee_payment_date)

        email_content = f"""
Dear {applicant.first_name} {applicant.last_name},

This email confirms that we have received your fee payment for the {application.program.name} program.

PAYMENT DETAILS:
• Application Number: {applicant.application_number}
• Program: {application.program.name}
• Amount Paid: ₹{payment_amount:,.2f}
• Transaction ID: {transaction_id}
• Payment Date: {payment_date.strftime('%B %d, %Y at %I:%M %p') if payment_date else 'N/A'}
• Payment Method: {payment_details.get('payment_method', 'Online')}

Your admission is now CONFIRMED! 

NEXT STEPS:
1. Download your official admission letter from the student portal
2. Report to the admission office with original documents
3. Complete the enrollment process before the session starts
4. Attend the orientation program (details will be shared separately)

IMPORTANT INFORMATION:
• Session Start Date: {application.admission_cycle.session_start_date}
• Orientation details will be emailed separately
• Keep this email as proof of payment

For any queries, please contact our admission office.

Congratulations and welcome to our university!

Best regards,
Admission Office
University ERP System

---
This is an automated email. Please do not reply to this email address.
"""

        # Send email
        send_mail(
            subject=subject,
            message=email_content,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'admissions@university.edu'),
            recipient_list=[applicant.email],
            fail_silently=False,
        )

        logger.info(f"Fee payment confirmation email sent to {applicant.email} for application {applicant.application_number}")
        return True

    except Exception as e:
        logger.error(f"Failed to send fee payment confirmation email: {str(e)}")
        return False
