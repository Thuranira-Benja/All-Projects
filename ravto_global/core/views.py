from django.shortcuts import render, get_object_or_404
from services.models import Service
from services.forms import ServiceRequestForm
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    services = Service.objects.all()
    return render(request, 'home.html', {'services': services})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def services_view(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})

def request_service(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            service_type = form.cleaned_data['service_type']
            location = form.cleaned_data['location']
            message_content = form.cleaned_data['message']

            subject = f"New Service Request: {service_type}"
            message = f"""
New Service Request Received:

Name: {name}
Phone: {phone}
Email: {email}
Location: {location}
Service Type: {service_type}
Message:
{message_content}
"""

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],  # send to yourself
                fail_silently=False,
            )

            return render(request, 'request_success.html')
    else:
        form = ServiceRequestForm()
    return render(request, 'request_service.html', {'form': form})


def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'service_detail.html', {'service': service})
