from django.shortcuts import render
from .models import Project

def projects_view(request):
    projects = Project.objects.filter(is_active=True)
    context = {
        'projects': projects,
    }
    return render(request, 'projects/projects.html', context)
