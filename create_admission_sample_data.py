"""
Sample data for testing admission management functionality
"""
from django.utils import timezone
from django.contrib.auth.models import User
from students.models import Program, Department
from admissions.models import AdmissionCycle, Applicant, Application

# Create sample data for testing
def create_sample_admission_data():
    # Create or get a user for decision making
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@university.edu',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()

    # Create or get department
    dept, created = Department.objects.get_or_create(
        name='Computer Science',
        defaults={
            'code': 'CS',
            'head_of_department': 'Dr. John Smith'
        }
    )

    # Create or get program
    program, created = Program.objects.get_or_create(
        name='Bachelor of Computer Science',
        defaults={
            'code': 'BCS',
            'department': dept,
            'duration_years': 4,
            'degree_type': 'undergraduate'
        }
    )

    # Create admission cycle
    cycle, created = AdmissionCycle.objects.get_or_create(
        name='Fall 2025 Admissions',
        defaults={
            'academic_year': '2025-2026',
            'application_start_date': timezone.now().date(),
            'application_end_date': timezone.now().date(),
            'session_start_date': timezone.now().date(),
            'is_active': True
        }
    )

    # Create sample applicants
    applicant1, created = Applicant.objects.get_or_create(
        application_number='APP2025001',
        defaults={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@email.com',
            'phone_number': '+1234567890',
            'date_of_birth': '2000-01-15',
            'gender': 'male',
            'category': 'general',
            'address_line1': '123 Main Street',
            'city': 'New York',
            'state': 'NY',
            'pincode': '10001',
            'guardian_name': 'Robert Doe',
            'guardian_relation': 'Father',
            'guardian_phone': '+1234567891'
        }
    )

    applicant2, created = Applicant.objects.get_or_create(
        application_number='APP2025002',
        defaults={
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@email.com',
            'phone_number': '+1234567892',
            'date_of_birth': '2000-03-20',
            'gender': 'female',
            'category': 'general',
            'address_line1': '456 Oak Avenue',
            'city': 'Los Angeles',
            'state': 'CA',
            'pincode': '90001',
            'guardian_name': 'Michael Smith',
            'guardian_relation': 'Father',
            'guardian_phone': '+1234567893'
        }
    )

    # Create sample applications
    application1, created = Application.objects.get_or_create(
        applicant=applicant1,
        program=program,
        admission_cycle=cycle,
        defaults={
            'status': 'submitted',
            'application_fee_paid': True,
            'application_fee_amount': 500.00,
            'previous_school_name': 'Central High School',
            'previous_school_board': 'State Board',
            'graduation_year': 2024,
            'overall_percentage': 88.5,
            'statement_of_purpose': 'I am passionate about computer science...',
            'admission_decision': 'pending'
        }
    )

    application2, created = Application.objects.get_or_create(
        applicant=applicant2,
        program=program,
        admission_cycle=cycle,
        defaults={
            'status': 'submitted',
            'application_fee_paid': True,
            'application_fee_amount': 500.00,
            'previous_school_name': 'Westfield High School',
            'previous_school_board': 'CBSE',
            'graduation_year': 2024,
            'overall_percentage': 92.0,
            'statement_of_purpose': 'Technology has always fascinated me...',
            'admission_decision': 'pending'
        }
    )

    print("Sample admission data created successfully!")
    print(f"Admin user: {admin_user.username} (password: admin123)")
    print(f"Applicants created: {applicant1.application_number}, {applicant2.application_number}")
    print(f"Program: {program.name}")
    print(f"Admission Cycle: {cycle.name}")

if __name__ == '__main__':
    create_sample_admission_data()
