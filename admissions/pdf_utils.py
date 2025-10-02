"""
PDF generation utilities for admission letters
"""
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from django.conf import settings
from django.utils import timezone
from io import BytesIO
import os

def generate_admission_letter_pdf(application):
    """
    Generate a provisional admission letter PDF for an admitted applicant
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)

    # Get styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )

    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        alignment=TA_CENTER,
        textColor=colors.darkred
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_LEFT
    )

    # Build the document content
    story = []

    # University Header
    story.append(Paragraph("UNIVERSITY ERP SYSTEM", title_style))
    story.append(Paragraph("PROVISIONAL ADMISSION LETTER", header_style))
    story.append(Spacer(1, 20))

    # Application details table
    app_data = [
        ["Application Number:", application.applicant.application_number],
        ["Date:", timezone.now().strftime("%B %d, %Y")],
        ["Academic Year:", application.admission_cycle.academic_year],
        ["Program:", application.program.name],
        ["Department:", application.program.department.name if hasattr(application.program, 'department') else "N/A"],
    ]

    app_table = Table(app_data, colWidths=[2*inch, 4*inch])
    app_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))

    story.append(app_table)
    story.append(Spacer(1, 20))

    # Applicant information
    story.append(Paragraph("Dear Mr./Ms. {} {},".format(
        application.applicant.first_name,
        application.applicant.last_name
    ), body_style))

    story.append(Spacer(1, 12))

    # Main content
    admission_text = """
    We are pleased to inform you that you have been <strong>PROVISIONALLY ADMITTED</strong> to the {} program 
    in the {} for the academic year {}.
    
    This admission is provisional and subject to:
    1. Verification of all submitted documents
    2. Payment of first semester fees
    3. Meeting all eligibility criteria
    4. Completion of the admission formalities within the specified deadline
    """.format(
        application.program.name,
        application.program.department.name if hasattr(application.program, 'department') else "University",
        application.admission_cycle.academic_year
    )

    story.append(Paragraph(admission_text, body_style))
    story.append(Spacer(1, 16))

    # Fee information
    if application.first_semester_fee_amount:
        fee_text = """
        <strong>First Semester Fee Details:</strong><br/>
        Amount: ₹{:,.2f}<br/>
        Status: {}
        """.format(
            application.first_semester_fee_amount,
            "PAID" if application.first_semester_fee_paid else "PENDING"
        )
        story.append(Paragraph(fee_text, body_style))
        story.append(Spacer(1, 16))

    # Important instructions
    instructions = """
    <strong>Important Instructions:</strong>
    
    1. This is a provisional admission letter. Final admission is subject to document verification and fee payment.
    2. Please report to the admission office within 7 days of receiving this letter.
    3. Bring all original documents for verification along with this letter.
    4. Pay the first semester fees to confirm your admission.
    5. Failure to complete the admission process within the deadline will result in cancellation of admission.
    
    For any queries, please contact the Admission Office.
    """

    story.append(Paragraph(instructions, body_style))
    story.append(Spacer(1, 30))

    # Signature section
    signature_data = [
        ["", ""],
        ["_________________________", "_________________________"],
        ["Admission Officer", "Registrar"],
        ["Date: {}".format(timezone.now().strftime("%B %d, %Y")), "University ERP System"],
    ]

    signature_table = Table(signature_data, colWidths=[3*inch, 3*inch])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 2), (-1, 3), 'Helvetica-Bold'),
        ('TOPPADDING', (0, 1), (-1, 1), 10),
    ]))

    story.append(signature_table)

    # Build the PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_fee_receipt_pdf(application, payment_details):
    """
    Generate a fee payment receipt PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )

    story = []

    # Header
    story.append(Paragraph("UNIVERSITY ERP SYSTEM", title_style))
    story.append(Paragraph("FEE PAYMENT RECEIPT", title_style))
    story.append(Spacer(1, 20))

    # Receipt details
    receipt_data = [
        ["Receipt No:", payment_details.get('receipt_number', 'N/A')],
        ["Date:", timezone.now().strftime("%B %d, %Y")],
        ["Student Name:", f"{application.applicant.first_name} {application.applicant.last_name}"],
        ["Application No:", application.applicant.application_number],
        ["Program:", application.program.name],
        ["Amount Paid:", f"₹{payment_details.get('amount', 0):,.2f}"],
        ["Payment Method:", payment_details.get('payment_method', 'N/A')],
        ["Transaction ID:", payment_details.get('transaction_id', 'N/A')],
    ]

    receipt_table = Table(receipt_data, colWidths=[2*inch, 4*inch])
    receipt_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    story.append(receipt_table)
    story.append(Spacer(1, 30))

    story.append(Paragraph("Thank you for your payment!", styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer
