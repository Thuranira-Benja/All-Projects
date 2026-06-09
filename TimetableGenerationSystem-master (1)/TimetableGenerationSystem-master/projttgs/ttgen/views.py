from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from .models import *
from .forms import *
from .render import Render

# Home view for "/"
def home(request):
    return render(request, 'home.html')

def view_timetable(request, timetable_id):
    timetable = get_object_or_404(ClassTimetable, pk=timetable_id)
    entries = TimetableEntry.objects.filter(timetable=timetable).order_by('meeting_time__day', 'meeting_time__time')
    days = {}
    for entry in entries:
        day = entry.meeting_time.day
        days.setdefault(day, []).append(entry)
    return render(request, 'timetable/view.html', {
        'timetable': timetable,
        'days': days
    })

def cbc_subject_list(request):
    subjects = CBCSubject.objects.all().order_by('level', 'name')
    return render(request, 'cbc_subject_list.html', {'subjects': subjects})

def add_cbc_subject(request):
    form = CBCSubjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('cbc_subject_list')
    return render(request, 'add_cbc_subject.html', {'form': form})

def teacher_list(request):
    teachers = Teacher.objects.all().order_by('name')
    return render(request, 'teacher_list.html', {'teachers': teachers})

def add_teacher(request):
    form = TeacherForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('teacher_list')
    return render(request, 'add_teacher.html', {'form': form})

def class_level_list(request):
    classes = ClassLevel.objects.all().order_by('level', 'name')
    return render(request, 'class_level_list.html', {'classes': classes})

def add_class_level(request):
    form = ClassLevelForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('class_level_list')
    return render(request, 'add_class_level.html', {'form': form})

def timetable_list(request):
    timetables = ClassTimetable.objects.all().order_by('-year', 'term', 'class_level')
    return render(request, 'timetable_list.html', {'timetables': timetables})

def create_timetable(request, class_level_id):
    class_level = get_object_or_404(ClassLevel, pk=class_level_id)
    form = ClassTimetableForm(request.POST or None, initial={'class_level': class_level})
    if form.is_valid():
        timetable = form.save(commit=False)
        timetable.class_level = class_level
        timetable.save()
        return redirect('view_timetable', timetable_id=timetable.id)
    return render(request, 'create_timetable.html', {
        'form': form,
        'class_level': class_level
    })

def generate_timetable(request, timetable_id):
    timetable = get_object_or_404(ClassTimetable, pk=timetable_id)
    # Timetable generation logic would go here
    return redirect('view_timetable', timetable_id=timetable.id)

class TimetablePDF(View):
    def get(self, request, timetable_id):
        timetable = get_object_or_404(ClassTimetable, pk=timetable_id)
        entries = TimetableEntry.objects.filter(timetable=timetable).order_by('meeting_time__day', 'meeting_time__time')
        days = {}
        for entry in entries:
            day = entry.meeting_time.day
            days.setdefault(day, []).append(entry)
        params = {
            'timetable': timetable,
            'days': days,
            'request': request
        }
        return Render.render('timetable_pdf.html', params)

def room_list(request):
    rooms = Room.objects.all().order_by('name')
    return render(request, 'room_list.html', {'rooms': rooms})

def add_room(request):
    form = RoomForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('room_list')
    return render(request, 'add_room.html', {'form': form})

def meeting_time_list(request):
    times = MeetingTime.objects.all().order_by('day', 'time')
    return render(request, 'meeting_time_list.html', {'times': times})

def add_meeting_time(request):
    form = MeetingTimeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('meeting_time_list')
    return render(request, 'add_meeting_time.html', {'form': form})
# Additional pages
def about(request):
    return render(request, 'about.html')

def help(request):
    return render(request, 'help.html')

def contact(request):
    return render(request, 'contact.html')

def login_view(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')
