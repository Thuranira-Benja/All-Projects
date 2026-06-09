from django.shortcuts import render, get_object_or_404
from .models import Department

def departments_list(request):
    departments = Department.objects.filter(is_active=True)
    context = {
        'departments': departments,
    }
    return render(request, 'departments/list.html', context)

def department_detail(request, slug):
    department = get_object_or_404(Department, slug=slug, is_active=True)
    context = {
        'department': department,
    }
    return render(request, 'departments/detail.html', context)
