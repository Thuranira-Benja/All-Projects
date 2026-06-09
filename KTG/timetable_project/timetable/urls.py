from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('generate/', views.generate_timetable_view, name='generate_timetable'),
    path('view/class/<int:class_id>/', views.view_class_timetable, name='view_class_timetable'),
    path('view/teacher/<int:teacher_id>/', views.view_teacher_timetable, name='view_teacher_timetable'),
    path('my-timetable/', views.my_timetable, name='my_timetable'),

    # Export routes
    path('export/class/<int:class_id>/pdf/', views.export_class_pdf, name='export_class_pdf'),
    path('export/class/<int:class_id>/excel/', views.export_class_excel, name='export_class_excel'),
    path('export/teacher/<int:teacher_id>/pdf/', views.export_teacher_pdf, name='export_teacher_pdf'),
    path('export/teacher/<int:teacher_id>/excel/', views.export_teacher_excel, name='export_teacher_excel'),

    # ✅ Admin Setup Guide
    path('admin-guide/', views.admin_guide, name='admin_guide'),
]
