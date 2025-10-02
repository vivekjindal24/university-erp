#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_erp.settings')
django.setup()

from admissions.models import Applicant, Application

try:
    # Get Kunal's application
    kunal = Applicant.objects.get(application_number='APP2025003')
    app = Application.objects.get(applicant=kunal)

    print("=" * 50)
    print("🎉 ADMISSION CONFIRMATION SUCCESS")
    print("=" * 50)
    print(f"Student Name: {kunal.first_name} {kunal.last_name}")
    print(f"Email Address: {kunal.email}")
    print(f"Application Number: {kunal.application_number}")
    print(f"Admission Status: {app.admission_decision.upper()}")
    print(f"Application Status: {app.status.upper()}")
    print(f"First Semester Fee: ₹{app.first_semester_fee_amount:,.2f}")
    print(f"Decision Date: {app.admission_decision_date}")
    print(f"Decision By: {app.admission_decision_by}")
    print("=" * 50)
    print("✅ EMAIL SENT TO: en22cs301541@medicaps.ac.in")
    print("📧 EMAIL SUBJECT: Admission Confirmation - Bachelor of Computer Science")
    print("=" * 50)

except Exception as e:
    print(f"Error: {e}")
