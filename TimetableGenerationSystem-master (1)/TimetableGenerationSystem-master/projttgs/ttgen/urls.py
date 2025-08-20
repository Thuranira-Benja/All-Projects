from django.urls import path
from . import views
from .views import TimetablePDF

urlpatterns = [
    path('', views.home, name='home'),  # 👈 Handles root "/"

    # CBC Curriculum
    path('cbc/subjects/', views.cbc_subject_list, name='cbc_subject_list'),
    path('cbc/subjects/add/', views.add_cbc_subject, name='add_cbc_subject'),

    # Teachers
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),

    # Classes
    path('classes/', views.class_level_list, name='class_level_list'),
    path('classes/add/', views.add_class_level, name='add_class_level'),

    # Timetables
    path('timetables/', views.timetable_list, name='timetable_list'),
    path('timetables/<int:class_level_id>/create/', views.create_timetable, name='create_timetable'),
    path('timetables/<int:timetable_id>/', views.view_timetable, name='view_timetable'),
    path('timetables/<int:timetable_id>/generate/', views.generate_timetable, name='generate_timetable'),
    path('timetables/<int:timetable_id>/pdf/', TimetablePDF.as_view(), name='timetable_pdf'),

    # Rooms
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.add_room, name='add_room'),

    # Meeting Times
    path('meeting-times/', views.meeting_time_list, name='meeting_time_list'),
    path('meeting-times/add/', views.add_meeting_time, name='add_meeting_time'),

    path('about/', views.about, name='about'),
    path('help/', views.help, name='help'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
]

