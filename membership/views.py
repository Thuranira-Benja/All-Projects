from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import MemberApplication

def register(request):
    """Member registration view"""
    if request.method == 'POST':
        # Get form data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth')
        profession = request.POST.get('profession')
        company = request.POST.get('company')
        job_title = request.POST.get('job_title')
        experience_years = request.POST.get('experience_years', 0)
        highest_qualification = request.POST.get('highest_qualification')
        institution = request.POST.get('institution')
        membership_type = request.POST.get('membership_type')
        department = request.POST.get('department')
        reason_for_joining = request.POST.get('reason_for_joining')
        expectations = request.POST.get('expectations')
        referral_source = request.POST.get('referral_source')
        referred_by = request.POST.get('referred_by')
        
        # Check if email already exists
        if MemberApplication.objects.filter(email=email).exists():
            messages.error(request, 'An application with this email already exists. Please use a different email or contact us.')
            return render(request, 'membership/register.html')
        
        try:
            # Create application
            application = MemberApplication.objects.create(
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                date_of_birth=date_of_birth if date_of_birth else None,
                profession=profession,
                company=company,
                job_title=job_title,
                experience_years=experience_years,
                highest_qualification=highest_qualification,
                institution=institution,
                membership_type=membership_type,
                department=department,
                reason_for_joining=reason_for_joining,
                expectations=expectations,
                referral_source=referral_source,
                referred_by=referred_by,
            )
            
            # Send confirmation email to applicant
            subject = "Membership Application Received - Meru Young Professionals"
            message = f"""
Dear {full_name},

Thank you for applying to join Meru Young Professionals (MYP)!

We have successfully received your membership application.

Application ID: MYP-{application.id:06d}
Membership Type: {membership_type.upper()}
Application Date: {application.created_at.strftime('%B %d, %Y')}

What happens next?
1. Our team will review your application within 5-7 business days
2. You will receive an email notification once your application is reviewed
3. If approved, you will receive your membership number and login credentials

If you have any questions, please don't hesitate to contact us at info@myp.or.ke

Best regards,
Meru Young Professionals Team
Empowering Professionals, Transforming Communities
"""
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            # Send notification to admin
            admin_subject = f"New Membership Application - {full_name}"
            admin_message = f"""
A new membership application has been submitted:

Applicant Information:
- Name: {full_name}
- Email: {email}
- Phone: {phone_number}
- Profession: {profession}
- Membership Type: {membership_type}

Please review this application in the admin panel.

Best regards,
MYP System
"""
            
            send_mail(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            
            messages.success(request, '✅ Your application has been submitted successfully! A confirmation email has been sent to your inbox.')
            return redirect('membership:success')
            
        except Exception as e:
            messages.error(request, '❌ There was an error submitting your application. Please try again or contact us directly.')
            return render(request, 'membership/register.html')
    
    return render(request, 'membership/register.html')

def success(request):
    """Registration success page"""
    return render(request, 'membership/success.html')