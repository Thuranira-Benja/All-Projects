from io import BytesIO
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from .models import TimeSlot


def get_structured_data(lessons):
    days = [d[0] for d in TimeSlot.DAY_CHOICES]

    # Get all unique time slots, avoiding duplicate start_times
    all_slots = TimeSlot.objects.filter(is_break=False).order_by('start_time', 'end_time')
    seen_times = set()
    slots = []
    for slot in all_slots:
        if slot.start_time not in seen_times:
            slots.append(slot)
            seen_times.add(slot.start_time)

    # First row: Header (Time slots)
    header = ['Day'] + [f"{slot.start_time:%H:%M}-{slot.end_time:%H:%M}" for slot in slots]
    data = [header]

    # Build each row per day
    for day in days:
        row = [day]
        for slot in slots:
            # Match exact slot and day
            lesson = lessons.filter(time_slot=slot, time_slot__day=day).first()
            if lesson:
                subject = lesson.subject_allocation.subject.name
                teacher = lesson.teacher.name
                row.append(f"{subject}\n({teacher})")
            else:
                row.append("")
        data.append(row)

    return data


def export_timetable_to_pdf(title, lessons):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []

    # ✅ Add class name as title
    styles = getSampleStyleSheet()
    title_para = Paragraph(f"<b>{title} Timetable</b>", styles['Title'])
    elements.append(title_para)
    elements.append(Spacer(1, 12))  # Add space after title

    data = get_structured_data(lessons)

    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (0, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return buffer


def export_timetable_to_excel(title, lessons):
    wb = Workbook()
    ws = wb.active
    ws.title = title

    data = get_structured_data(lessons)

    for row in data:
        ws.append(row)

    return wb
