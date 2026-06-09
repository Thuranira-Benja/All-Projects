from django.shortcuts import render
from .models import Event

def events_view(request):
    events = Event.objects.all()
    context = {
        'events': events,
    }
    return render(request, 'events/events.html', context)
