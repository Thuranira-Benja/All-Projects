from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import SchoolClass, Teacher, TimeSlot, Lesson, Student
from .generator import TimetableGenerator
from .exports import export_timetable_to_pdf, export_timetable_to_excel

# ✅ Helper to structure timetable data into grid format
def get_timetable_data(lessons):
    days = [day[0] for day in TimeSlot.DAY_CHOICES]
    all_slots = TimeSlot.objects.filter(is_break=False).order_by('start_time', 'end_time')

    seen_times = set()
    slots = []
    for slot in all_slots:
        if slot.start_time not in seen_times:
            slots.append(slot)
            seen_times.add(slot.start_time)

    grid = {slot: {day: None for day in days} for slot in slots}

    for lesson in lessons:
        if lesson.time_slot in grid:
            grid[lesson.time_slot][lesson.time_slot.day] = lesson

    return {
        'grid': grid,
        'slots': slots,
        'days': days
    }

# ✅ Admin Dashboard View
@staff_member_required
def dashboard(request):
    classes = SchoolClass.objects.all()
    teachers = Teacher.objects.all()

    # Display generation result messages
    success = request.session.pop('generation_success', False)
    error = request.session.pop('generation_error', '')

    context = {
        'classes': classes,
        'teachers': teachers,
        'generation_success': success,
        'generation_error': error
    }
    return render(request, 'timetable/dashboard.html', context)

# ✅ Handle Timetable Generation
@staff_member_required
def generate_timetable_view(request):
    if request.method == 'POST':
        Lesson.objects.all().delete()
        classes_to_generate = SchoolClass.objects.all()
        generator = TimetableGenerator(classes_to_generate)
        success = generator.generate()

        if success:
            request.session['generation_success'] = True
        else:
            request.session['generation_error'] = 'Some lessons could not be scheduled due to constraints.'

        return redirect('dashboard')

    return render(request, 'timetable/generate.html')

# ✅ View a Class Timetable
@staff_member_required
def view_class_timetable(request, class_id):
    s_class = get_object_or_404(SchoolClass, id=class_id)
    lessons = Lesson.objects.filter(school_class=s_class).order_by('time_slot__day', 'time_slot__start_time')
    context = {
        'timetable_type': 'Class',
        'item_name': s_class.name,
        'item_id': s_class.id,
        **get_timetable_data(lessons)
    }
    return render(request, 'timetable/timetable_view.html', context)

# ✅ View a Teacher Timetable
@staff_member_required
def view_teacher_timetable(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    lessons = Lesson.objects.filter(teacher=teacher).order_by('time_slot__day', 'time_slot__start_time')
    context = {
        'timetable_type': 'Teacher',
        'item_name': teacher.name,
        'item_id': teacher.id,
        **get_timetable_data(lessons)
    }
    return render(request, 'timetable/timetable_view.html', context)

# ✅ Parent/Student View Own Timetable
@login_required
def my_timetable(request):
    try:
        student = Student.objects.get(parent=request.user)
        return redirect('view_class_timetable', class_id=student.school_class.id)
    except Student.DoesNotExist:
        return render(request, 'timetable/no_timetable.html')

# ✅ Export Class Timetable to PDF
@staff_member_required
def export_class_pdf(request, class_id):
    s_class = get_object_or_404(SchoolClass, id=class_id)
    lessons = Lesson.objects.filter(school_class=s_class)
    buffer = export_timetable_to_pdf(s_class.name, lessons)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{s_class.name}_timetable.pdf"'
    return response

# ✅ Export Class Timetable to Excel
@staff_member_required
def export_class_excel(request, class_id):
    s_class = get_object_or_404(SchoolClass, id=class_id)
    lessons = Lesson.objects.filter(school_class=s_class)
    workbook = export_timetable_to_excel(s_class.name, lessons)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{s_class.name}_timetable.xlsx"'
    workbook.save(response)
    return response

# ✅ Export Teacher Timetable to PDF
@staff_member_required
def export_teacher_pdf(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    lessons = Lesson.objects.filter(teacher=teacher)
    buffer = export_timetable_to_pdf(teacher.name, lessons)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{teacher.name}_timetable.pdf"'
    return response

# ✅ Export Teacher Timetable to Excel
@staff_member_required
def export_teacher_excel(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    lessons = Lesson.objects.filter(teacher=teacher)
    workbook = export_timetable_to_excel(teacher.name, lessons)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{teacher.name}_timetable.xlsx"'
    workbook.save(response)
    return response

# ✅ Admin Setup Guide View
@staff_member_required
def admin_guide(request):
    return render(request, 'timetable/admin_guide.html')
