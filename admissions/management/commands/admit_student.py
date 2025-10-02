"""
Django management command to admit an applicant and send confirmation email
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from admissions.models import Applicant, Application
from admissions.email_utils import send_admission_confirmation_email

class Command(BaseCommand):
    help = 'Admit an applicant and send confirmation email'

    def add_arguments(self, parser):
        parser.add_argument(
            '--application-number',
            type=str,
            default='APP2025003',
            help='Application number of the student to admit'
        )
        parser.add_argument(
            '--fee-amount',
            type=float,
            default=75000.00,
            help='First semester fee amount'
        )

    def handle(self, *args, **options):
        application_number = options['application_number']
        fee_amount = options['fee_amount']

        try:
            # Get the applicant
            applicant = Applicant.objects.get(application_number=application_number)
            self.stdout.write(f"Found applicant: {applicant.first_name} {applicant.last_name}")
            self.stdout.write(f"Email: {applicant.email}")

            # Get the application
            application = Application.objects.get(applicant=applicant)
            self.stdout.write(f"Application status: {application.admission_decision}")

            if application.admission_decision == 'admitted':
                self.stdout.write(
                    self.style.WARNING(f'Student {applicant.first_name} {applicant.last_name} is already admitted!')
                )
                return

            # Get or create admin user for decision tracking
            admin_user, created = User.objects.get_or_create(
                username='admin',
                defaults={'is_staff': True, 'is_superuser': True}
            )

            # Update application status to admitted
            application.admission_decision = 'admitted'
            application.status = 'admitted'
            application.admission_decision_date = timezone.now()
            application.admission_decision_by = admin_user
            application.first_semester_fee_amount = fee_amount
            application.save()

            self.stdout.write(
                self.style.SUCCESS(f'✅ {applicant.first_name} {applicant.last_name} has been admitted!')
            )
            self.stdout.write(f"First semester fee set to: ₹{fee_amount:,.2f}")

            # Send admission confirmation email
            self.stdout.write("Sending admission confirmation email...")

            email_sent = send_admission_confirmation_email(application)

            if email_sent:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Admission confirmation email sent successfully to {applicant.email}!')
                )
                self.stdout.write("Email contents:")
                self.stdout.write("=" * 50)
                self.stdout.write(f"To: {applicant.email}")
                self.stdout.write(f"Subject: Admission Confirmation - {application.program.name}")
                self.stdout.write("=" * 50)
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Failed to send email to {applicant.email}')
                )
                self.stdout.write("Please check your email configuration in .env file")

        except Applicant.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ Applicant with application number {application_number} not found!')
            )

        except Application.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ Application not found for applicant {application_number}!')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )
