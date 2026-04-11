from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import os


def create_certificate(pdf_path, student_data, request_data, signature_path, qr_path, certificate_id, timestamp, hod_name='HOD'):
    """
    Generate a certificate PDF with student details, HOD signature, and QR code.
    
    Args:
        pdf_path: Path to save the PDF
        student_data: Dictionary containing student details (name, usn, department, etc.)
        request_data: Dictionary containing request details (request_type, reason, etc.)
        signature_path: Path to HOD's signature image
        qr_path: Path to QR code image
        certificate_id: Unique certificate identifier
        timestamp: Date/time string
        hod_name: Name of the HOD signing the certificate (default: 'HOD')
    """
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, 
                           rightMargin=50, leftMargin=50, 
                           topMargin=50, bottomMargin=50)
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=20,
        alignment=1,  # Center
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=10,
        textColor=colors.darkblue
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=8
    )
    
    elements = []
    
    # Title
    elements.append(Paragraph("OFFICIAL CERTIFICATE", title_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Certificate ID: {certificate_id}", heading_style))
    elements.append(Spacer(1, 30))
    
    # Student Details Section
    elements.append(Paragraph("<b>STUDENT DETAILS</b>", heading_style))
    elements.append(Spacer(1, 10))
    
    student_details = [
        ["Name:", student_data.get('name', 'N/A')],
        ["USN:", student_data.get('usn', 'N/A')],
        ["Department:", student_data.get('department', 'N/A')],
        ["Semester:", str(student_data.get('semester', 'N/A'))],
        ["Register Number:", request_data.get('register_number', 'N/A')],
        ["Email:", student_data.get('email', 'N/A')],
    ]
    
    student_table = Table(student_details, colWidths=[2*inch, 4*inch])
    student_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(student_table)
    elements.append(Spacer(1, 25))
    
    # Request Details Section
    elements.append(Paragraph("<b>REQUEST DETAILS</b>", heading_style))
    elements.append(Spacer(1, 10))
    
    request_details = [
        ["Request Type:", request_data.get('request_type', 'N/A')],
        ["Course:", request_data.get('course', 'N/A')],
        ["Faculty:", request_data.get('faculty', 'N/A')],
        ["Batch:", request_data.get('batch', 'N/A')],
        ["Study Mode:", request_data.get('study_mode', 'N/A')],
        ["Mobile:", request_data.get('mobile_number', 'N/A')],
        ["Reason:", request_data.get('reason', 'N/A')],
    ]
    
    request_table = Table(request_details, colWidths=[2*inch, 4*inch])
    request_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(request_table)
    elements.append(Spacer(1, 25))
    
    # Approval Info
    elements.append(Paragraph("<b>APPROVAL INFORMATION</b>", heading_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Date of Issue: {timestamp}", normal_style))
    elements.append(Paragraph("Status: APPROVED", normal_style))
    elements.append(Spacer(1, 40))
    
    # HOD Signature Section
    elements.append(Paragraph("<b>HOD Signature:</b>", normal_style))
    elements.append(Spacer(1, 10))
    
    if os.path.exists(signature_path):
        signature_img = Image(signature_path, width=200, height=80)
        elements.append(signature_img)
    
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(f"<i>{hod_name}</i>", normal_style))
    elements.append(Spacer(1, 30))
    
    # QR Code Section
    elements.append(Paragraph("<b>Scan to Verify:</b>", normal_style))
    elements.append(Spacer(1, 10))
    
    if os.path.exists(qr_path):
        qr_img = Image(qr_path, width=100, height=100)
        elements.append(qr_img)
    
    # Build PDF
    doc.build(elements)
    return pdf_path