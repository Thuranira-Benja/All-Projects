from django.shortcuts import render
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
            # Collect form data manually
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email_address = form.cleaned_data['email']
            service_type = form.cleaned_data['service_type']
            location = form.cleaned_data['location']
            message_content = form.cleaned_data['message']

            subject = f"New Service Request: {service_type}"
            message = f"""
New Service Request Received:

Name: {name}
Phone: {phone}
Email: {email_address}
Location: {location}
Service Type: {service_type}
Message:
{message_content}
"""

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                ['benjaminlamata@gmail.com'],  # receiver email
                fail_silently=False,
            )

            return render(request, 'request_success.html')
    else:
        form = ServiceRequestForm()
    return render(request, 'request_service.html', {'form': form})
