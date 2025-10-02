#!/usr/bin/env python
"""
Complete verification script for Kunal Tomar's admission process
"""
import os
import django
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_erp.settings')
django.setup()

from admissions.models import Applicant, Application
from admissions.email_utils import send_admission_confirmation_email
from django.contrib.auth.models import User

def main():
    try:
        print("🔍 CHECKING KUNAL TOMAR'S APPLICATION STATUS...")
        print("=" * 60)

        # Get Kunal's records
        kunal = Applicant.objects.get(application_number='APP2025003')
        app = Application.objects.get(applicant=kunal)

        print(f"✅ Found Student: {kunal.first_name} {kunal.last_name}")
        print(f"📧 Email Address: {kunal.email}")
        print(f"🔢 Application Number: {kunal.application_number}")
        print(f"📊 Current Admission Status: {app.admission_decision}")
        print(f"💰 First Semester Fee: ₹{app.first_semester_fee_amount or 0:,.2f}")

        # If not admitted, admit the student
        if app.admission_decision != 'admitted':
            print("\n🎯 ADMITTING STUDENT...")

            # Get admin user
            admin_user, created = User.objects.get_or_create(
                username='admin',
                defaults={'is_staff': True, 'is_superuser': True}
            )

            # Update admission status
            app.admission_decision = 'admitted'
            app.status = 'admitted'
            app.admission_decision_date = timezone.now()
            app.admission_decision_by = admin_user
            app.first_semester_fee_amount = 75000.00
            app.save()

            print("✅ Student status updated to ADMITTED")
            print(f"💰 First semester fee set to: ₹{app.first_semester_fee_amount:,.2f}")

            # Send admission email
            print("\n📧 SENDING ADMISSION CONFIRMATION EMAIL...")
            email_sent = send_admission_confirmation_email(app)

            if email_sent:
                print(f"✅ SUCCESS: Email sent to {kunal.email}")
                print(f"📬 Subject: Admission Confirmation - {app.program.name}")
            else:
                print(f"❌ FAILED: Could not send email to {kunal.email}")
                print("Please check your .env file email configuration")

        else:
            print(f"\n✅ STUDENT ALREADY ADMITTED")
            print(f"📅 Admission Date: {app.admission_decision_date}")
            print(f"👤 Admitted By: {app.admission_decision_by}")

        print("\n" + "=" * 60)
        print("🎉 FINAL STATUS SUMMARY")
        print("=" * 60)
        print(f"Student: {kunal.first_name} {kunal.last_name}")
        print(f"Email: {kunal.email}")
        print(f"Status: {app.admission_decision.upper()}")
        print(f"Fee Amount: ₹{app.first_semester_fee_amount:,.2f}")
        print(f"Program: {app.program.name}")
        print("=" * 60)

        if app.admission_decision == 'admitted':
            print("🎊 CONGRATULATIONS! Kunal Tomar has been successfully admitted!")
            print(f"📧 Confirmation email sent to: {kunal.email}")

    except Applicant.DoesNotExist:
        print("❌ ERROR: Kunal Tomar's application not found!")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    main()
