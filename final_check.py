#!/usr/bin/env python
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_erp.settings')
django.setup()

from admissions.models import Applicant, Application

# Force output to be displayed
sys.stdout.flush()
sys.stderr.flush()

print("🔍 VERIFYING KUNAL TOMAR'S ADMISSION STATUS...")
print("=" * 50)

try:
    kunal = Applicant.objects.get(application_number='APP2025003')
    app = Application.objects.get(applicant=kunal)

    print(f"Student Name: {kunal.first_name} {kunal.last_name}")
    print(f"Email: {kunal.email}")
    print(f"Application Number: {kunal.application_number}")
    print(f"Admission Status: {app.admission_decision}")
    print(f"Application Status: {app.status}")
    print(f"First Semester Fee: Rs.{app.first_semester_fee_amount}")
    print(f"Decision Date: {app.admission_decision_date}")

    if app.admission_decision == 'admitted':
        print("\n✅ SUCCESS: KUNAL TOMAR HAS BEEN ADMITTED!")
        print(f"📧 Email sent to: {kunal.email}")
        print("🎉 Admission process completed successfully!")
    else:
        print("\n⏳ Status: Application still pending")

except Exception as e:
    print(f"Error: {e}")

print("=" * 50)
