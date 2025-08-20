import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def generate_permit_pdf(permit):
    """Generates a PDF for a given business permit and returns it as a bytes object."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    
    # Title
    c.setFont('Helvetica-Bold', 20, leading=None)
    c.drawCentredString(4.25 * inch, 1 * inch, "MERU COUNTY BUSINESS PERMIT")
    
    # Details
    c.setFont('Helvetica', 12, leading=None)
    text_y = 2.5 * inch
    c.drawString(1 * inch, text_y, f"Permit ID: {permit.id}")
    c.drawString(1 * inch, text_y + 20, f"Business Name: {permit.business_name}")
    c.drawString(1 * inch, text_y + 40, f"Owner: {permit.owner.get_full_name() or permit.owner.username}")
    c.drawString(1 * inch, text_y + 60, f"Ward: {permit.ward}")
    c.drawString(1 * inch, text_y + 80, f"Issue Date: {permit.issue_date.strftime('%d-%b-%Y')}")
    c.drawString(1 * inch, text_y + 100, f"Expiry Date: {permit.expiry_date.strftime('%d-%b-%Y')}")
    c.drawString(1 * inch, text_y + 120, f"Receipt No: {permit.receipt_no}")
    
    # Watermark/Footer
    c.setFont('Helvetica-Oblique', 8, leading=None)
    c.drawCentredString(4.25 * inch, 10 * inch, "Official Document - Meru eCitizen Hub")

    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer