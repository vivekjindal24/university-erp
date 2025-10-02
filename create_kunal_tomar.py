"""
Create Kunal Tomar applicant for testing admission management
"""
from django.utils import timezone
from django.contrib.auth.models import User
from students.models import Program, Department
from admissions.models import AdmissionCycle, Applicant, Application

def create_kunal_tomar_applicant():
    # Get existing program and cycle
    try:
        program = Program.objects.get(name='Bachelor of Computer Science')
        cycle = AdmissionCycle.objects.get(name='Fall 2025 Admissions')
    except:
        print("Error: Please run the main sample data script first")
        return

    # Create Kunal Tomar applicant
    applicant, created = Applicant.objects.get_or_create(
        application_number='APP2025003',
        defaults={
            'first_name': 'Kunal',
            'last_name': 'Tomar',
            'email': 'kunal.tomar@email.com',
            'phone_number': '+919876543210',
            'date_of_birth': '2001-05-10',
            'gender': 'male',
            'category': 'general',
            'address_line1': '789 Park Street',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'pincode': '400001',
            'country': 'India',
            'guardian_name': 'Rajesh Tomar',
            'guardian_relation': 'Father',
            'guardian_phone': '+919876543211'
        }
    )

    # Create application for Kunal Tomar
    application, created = Application.objects.get_or_create(
        applicant=applicant,
        program=program,
        admission_cycle=cycle,
        defaults={
            'status': 'submitted',
            'application_fee_paid': True,
            'application_fee_amount': 500.00,
            'previous_school_name': 'Delhi Public School',
            'previous_school_board': 'CBSE',
            'graduation_year': 2024,
            'overall_percentage': 89.2,
            'statement_of_purpose': 'I am passionate about software development and want to contribute to the tech industry...',
            'admission_decision': 'pending'  # This is key - must be 'pending' to show Admit button
        }
    )

    if created:
        print(f"✅ Created new applicant: {applicant.first_name} {applicant.last_name}")
        print(f"📧 Application Number: {applicant.application_number}")
        print(f"📝 Application Status: {application.admission_decision}")
        print(f"💰 Application Fee: ₹{application.application_fee_amount}")
    else:
        print(f"✅ Applicant already exists: {applicant.first_name} {applicant.last_name}")
        print(f"📧 Application Number: {applicant.application_number}")
        print(f"📝 Current Status: {application.admission_decision}")

if __name__ == '__main__':
    create_kunal_tomar_applicant()
