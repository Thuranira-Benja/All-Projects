from django.shortcuts import render
from .models import Constitution

def constitution_view(request):
    constitution = Constitution.objects.filter(is_active=True).first()
    context = {
        'constitution': constitution,
    }
    return render(request, 'constitution/constitution.html', context)
