from django.shortcuts import render
from .models import Leadership, Council

def leadership_view(request):
    leaders = Leadership.objects.filter(is_active=True)
    council = Council.objects.filter(is_active=True)
    
    context = {
        'leaders': leaders,
        'council': council,
    }
    return render(request, 'leadership/leadership.html', context)
