import os
from io import BytesIO
from celery import shared_task
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .models import BusinessPermit

@shared_task
def generate_and_save_permit_pdf_task(permit_id):
    try:
        permit = BusinessPermit.objects.get(id=permit_id)

        context = {
            'permit': permit
        }

        html = render_to_string('licensing/permit_template.html', context)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

        if not pdf.err:
            file_name = f"permit_{permit.id}.pdf"
            permit.permit_pdf.save(file_name, ContentFile(result.getvalue()))
            permit.save()
        else:
            print(f"Error generating PDF for permit {permit.id}")
    except BusinessPermit.DoesNotExist:
        print(f"Permit with id {permit_id} does not exist.")
