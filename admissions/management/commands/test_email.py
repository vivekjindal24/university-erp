"""
Email Test Command for University ERP System
Run this to test if Gmail email configuration is working
"""
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Test email configuration by sending a test email'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to-email',
            type=str,
            default='jindal.vi@northeastern.edu',
            help='Email address to send test email to'
        )

    def handle(self, *args, **options):
        to_email = options['to_email']

        self.stdout.write(f"Testing email configuration...")
        self.stdout.write(f"From: {settings.EMAIL_HOST_USER}")
        self.stdout.write(f"To: {to_email}")

        try:
            send_mail(
                subject='Test Email - University ERP System',
                message='''
This is a test email from your University ERP System.

If you received this email, your Gmail SMTP configuration is working correctly!

Email Configuration Details:
- SMTP Host: smtp.gmail.com
- Port: 587
- TLS: Enabled
- From: {from_email}

You can now use the admission system to send real emails to students.

Best regards,
University ERP System
                '''.format(from_email=settings.EMAIL_HOST_USER),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[to_email],
                fail_silently=False,
            )

            self.stdout.write(
                self.style.SUCCESS(f'✅ Test email sent successfully to {to_email}!')
            )
            self.stdout.write(
                self.style.SUCCESS('Gmail configuration is working correctly.')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to send test email: {str(e)}')
            )
            self.stdout.write(
                self.style.ERROR('Please check your Gmail app password and configuration.')
            )
