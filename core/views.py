from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import SiteConfiguration, Stat, CoreValue, Project, Event, BlogPost, Partner, Leader, GalleryImage, Constitution

def home(request):
    from departments.models import Department
    config = SiteConfiguration.objects.first()
    if not config:
        config = SiteConfiguration.objects.create()
    context = {
        'site_config': config,
        'stats': Stat.objects.filter(is_active=True),
        'core_values': CoreValue.objects.filter(is_active=True),
        'departments': Department.objects.filter(is_active=True)[:6],
        'featured_projects': Project.objects.filter(is_featured=True)[:3],
        'upcoming_events': Event.objects.filter(is_featured=True)[:3],
        'latest_posts': BlogPost.objects.filter(is_published=True)[:3],
        'partners': Partner.objects.filter(is_active=True),
        'member_count': 1200,
    }
    return render(request, 'core/home.html', context)

def about(request):
    config = SiteConfiguration.objects.first()
    return render(request, 'core/about.html', {'site_config': config})

def mission(request):
    config = SiteConfiguration.objects.first()
    core_values = CoreValue.objects.filter(is_active=True)
    return render(request, 'core/mission.html', {'site_config': config, 'core_values': core_values})

def leadership(request):
    config = SiteConfiguration.objects.first()
    council = Leader.objects.filter(category='council', is_active=True)
    department_leaders = Leader.objects.filter(category='department', is_active=True)
    context = {
        'site_config': config,
        'council': council,
        'department_leaders': department_leaders,
    }
    return render(request, 'core/leadership.html', context)

def departments(request):
    from departments.models import Department
    config = SiteConfiguration.objects.first()
    departments = Department.objects.filter(is_active=True)
    context = {
        'site_config': config,
        'departments': departments,
    }
    return render(request, 'core/departments.html', context)

def department_detail(request, slug):
    from departments.models import Department
    config = SiteConfiguration.objects.first()
    department = get_object_or_404(Department, slug=slug, is_active=True)
    context = {
        'site_config': config,
        'department': department,
    }
    return render(request, 'core/department_detail.html', context)

def projects(request):
    config = SiteConfiguration.objects.first()
    projects = Project.objects.all()
    return render(request, 'core/projects.html', {'site_config': config, 'projects': projects})

def events(request):
    config = SiteConfiguration.objects.first()
    events = Event.objects.all()
    return render(request, 'core/events.html', {'site_config': config, 'events': events})

def blog(request):
    config = SiteConfiguration.objects.first()
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, 'core/blog.html', {'site_config': config, 'posts': posts})

def blog_detail(request, slug):
    config = SiteConfiguration.objects.first()
    post = BlogPost.objects.get(slug=slug)
    post.views += 1
    post.save()
    return render(request, 'core/blog_detail.html', {'site_config': config, 'post': post})

def gallery(request):
    config = SiteConfiguration.objects.first()
    images = GalleryImage.objects.all()
    return render(request, 'core/gallery.html', {'site_config': config, 'images': images})

def constitution(request):
    config = SiteConfiguration.objects.first()
    constitution = Constitution.objects.filter(is_active=True).first()
    return render(request, 'core/constitution.html', {'site_config': config, 'constitution': constitution})

def contact(request):
    config = SiteConfiguration.objects.first()
    return render(request, 'core/contact.html', {'site_config': config})

def leadership_apply(request):
    config = SiteConfiguration.objects.first()
    context = {
        'site_config': config,
    }
    return render(request, 'core/leadership_apply.html', context)

def leadership_apply_submit(request):
    if request.method == 'POST':
        messages.success(request, 'Thank you for your application! Our team will review it and get back to you soon.')
        return redirect('core:leadership')
    return redirect('core:leadership')

def proposal_form(request):
    """Project proposal form page"""
    config = SiteConfiguration.objects.first()
    context = {
        'site_config': config,
    }
    return render(request, 'core/proposal_form.html', context)

def submit_proposal(request):
    """Process project proposal submission"""
    if request.method == 'POST':
        # Get form data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        membership_id = request.POST.get('membership_id')
        project_title = request.POST.get('project_title')
        project_category = request.POST.get('project_category')
        project_description = request.POST.get('project_description')
        location = request.POST.get('location')
        duration = request.POST.get('duration')
        beneficiaries = request.POST.get('beneficiaries')
        budget = request.POST.get('budget')
        resources = request.POST.get('resources')
        partners = request.POST.get('partners')
        start_date = request.POST.get('start_date')
        milestones = request.POST.get('milestones')
        why_support = request.POST.get('why_support')
        experience = request.POST.get('experience')
        comments = request.POST.get('comments')
        
        # Prepare email content
        subject = f"New Project Proposal: {project_title} from {full_name}"
        
        message = f"""
        ========================================
        NEW PROJECT PROPOSAL SUBMISSION
        ========================================
        
        SUBMITTER INFORMATION:
        ----------------------
        Name: {full_name}
        Email: {email}
        Phone: {phone if phone else 'Not provided'}
        MYP Membership ID: {membership_id if membership_id else 'Not provided'}
        
        PROJECT INFORMATION:
        -------------------
        Title: {project_title}
        Category: {project_category}
        Location: {location}
        Estimated Duration: {duration if duration else 'Not specified'}
        
        Description:
        {project_description}
        
        IMPACT & RESOURCES:
        ------------------
        Expected Beneficiaries: {beneficiaries if beneficiaries else 'Not specified'}
        Estimated Budget: KSH {budget if budget else 'Not specified'}
        
        Resources Needed:
        {resources if resources else 'Not specified'}
        
        Partners/Collaborators:
        {partners if partners else 'Not specified'}
        
        TIMELINE:
        ---------
        Proposed Start Date: {start_date if start_date else 'Not specified'}
        
        Key Milestones:
        {milestones if milestones else 'Not specified'}
        
        ADDITIONAL INFORMATION:
        -----------------------
        Why MYP Should Support:
        {why_support if why_support else 'Not specified'}
        
        Previous Experience:
        {experience if experience else 'Not specified'}
        
        Additional Comments:
        {comments if comments else 'Not specified'}
        
        ========================================
        Please review this proposal and follow up with the submitter.
        ========================================
        """
        
        try:
            # Send email to admin
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            
            # Also send confirmation to submitter
            confirmation_message = f"""
            Dear {full_name},
            
            Thank you for submitting your project proposal "{project_title}" to Meru Young Professionals.
            
            We have received your proposal and our team will review it within 5-7 business days. 
            We will contact you at {email} with feedback or next steps.
            
            If you have any questions, please don't hesitate to contact us at info@myp.or.ke.
            
            Best regards,
            Meru Young Professionals Team
            """
            
            send_mail(
                f"Proposal Received: {project_title}",
                confirmation_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Thank you for your proposal! We have received your submission and will review it shortly. A confirmation email has been sent to your inbox.')
            
        except Exception as e:
            messages.error(request, 'There was an error submitting your proposal. Please try again or contact us directly at info@myp.or.ke.')
        
        return redirect('core:projects')
    
    return redirect('core:projects')

def contact_submit(request):
    """Process contact form submission"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        newsletter = request.POST.get('newsletter')
        
        # Validate required fields
        if not name or not email or not subject or not message:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('core:contact')
        
        try:
            # Send email to admin
            email_subject = f"Contact Form: {subject} from {name}"
            email_message = f"""
            Name: {name}
            Email: {email}
            Phone: {phone if phone else 'Not provided'}
            Newsletter: {'Yes' if newsletter else 'No'}
            
            Message:
            {message}
            """
            
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            
            # Send auto-reply to user
            auto_reply = f"""
            Dear {name},
            
            Thank you for contacting Meru Young Professionals. We have received your message and will get back to you within 2-3 business days.
            
            Best regards,
            Meru Young Professionals Team
            """
            
            send_mail(
                f"Thank you for contacting MYP - {subject}",
                auto_reply,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again or call us directly.')
        
        return redirect('core:contact')
    
    return redirect('core:contact')

def contact(request):
    config = SiteConfiguration.objects.first()
    context = {
        'site_config': config,
    }
    return render(request, 'core/contact.html', context)

def contact_submit(request):
    """Process contact form submission"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        newsletter = request.POST.get('newsletter')
        
        # Validate required fields
        if not name or not email or not subject or not message:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('core:contact')
        
        try:
            # Send email to admin
            email_subject = f"Contact Form: {subject} from {name}"
            email_message = f"""
            Name: {name}
            Email: {email}
            Phone: {phone if phone else 'Not provided'}
            Newsletter: {'Yes' if newsletter else 'No'}
            
            Message:
            {message}
            """
            
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            
            # Send auto-reply to user
            auto_reply = f"""
            Dear {name},
            
            Thank you for contacting Meru Young Professionals. We have received your message and will get back to you within 2-3 business days.
            
            Best regards,
            Meru Young Professionals Team
            """
            
            send_mail(
                f"Thank you for contacting MYP - {subject}",
                auto_reply,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again or call us directly.')
        
        return redirect('core:contact')
    
    return redirect('core:contact')
