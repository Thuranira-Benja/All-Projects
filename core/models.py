from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class SiteConfiguration(models.Model):
    """Main site configuration - everything is dynamic"""
    # Logo and Branding
    logo = models.ImageField(upload_to='logo/', help_text="Main logo (recommended: 200x60px)", blank=True, null=True)
    logo_footer = models.ImageField(upload_to='logo/', help_text="Footer logo (recommended: 150x50px)", blank=True, null=True)
    favicon = models.ImageField(upload_to='logo/', help_text="Browser tab icon", blank=True, null=True)
    
    # Hero Section
    hero_type = models.CharField(max_length=20, choices=[('image', 'Image'), ('video', 'Video')], default='image')
    hero_background = models.ImageField(upload_to='hero/', help_text="Hero background image (1920x1080px)", blank=True, null=True)
    hero_video = models.FileField(upload_to='hero/', help_text="Hero background video (MP4 format)", blank=True, null=True)
    hero_tagline = models.CharField(max_length=100, default="MT. KENYA · NON-PROFIT · YOUTH-LED")
    hero_title_line1 = models.CharField(max_length=100, default="Empowering")
    hero_title_line2 = models.CharField(max_length=100, default="Professionals")
    hero_title_line3 = models.CharField(max_length=100, default="Transforming Communities")
    hero_subtitle = models.TextField(default="Meru Young Professionals unites a generation of leaders, innovators and changemakers from the Mt. Kenya region and beyond.")
    
    # Buttons
    become_member_text = models.CharField(max_length=50, default="Become a Member")
    become_member_url = models.CharField(max_length=200, default="/members/register/")
    join_us_text = models.CharField(max_length=50, default="Join Us")
    join_us_url = models.CharField(max_length=200, default="/members/register/")
    
    # Welcome Section
    welcome_title = models.CharField(max_length=200, default="A network rooted in Mt. Kenya, reaching nation-wide.")
    welcome_content = RichTextUploadingField(default="We bring together young professionals committed to leadership, innovation, entrepreneurship, mentorship, environmental conservation and economic empowerment — anchored in service and excellence.")
    learn_more_url = models.CharField(max_length=200, default="/about/")
    
    # Cards Content
    mission_text = models.TextField(default="Empower young professionals through leadership, innovation and service.")
    vision_text = models.TextField(default="The leading network of transformative professionals across Kenya.")
    community_text = models.CharField(max_length=200, default="1,200+ professionals collaborating to drive measurable impact.")
    innovation_text = models.CharField(max_length=200, default="Bold ideas, applied locally for lasting transformation.")
    
    # Section Titles
    core_values_title = models.CharField(max_length=100, default="CORE VALUES")
    core_values_subtitle = models.CharField(max_length=200, default="The principles that guide every member")
    departments_title = models.CharField(max_length=100, default="DEPARTMENTS")
    departments_subtitle = models.CharField(max_length=200, default="Where impact takes shape")
    projects_title = models.CharField(max_length=100, default="FEATURED PROJECTS")
    projects_subtitle = models.CharField(max_length=200, default="Building tomorrow, today.")
    events_title = models.CharField(max_length=100, default="UPCOMING EVENTS")
    events_subtitle = models.CharField(max_length=200, default="Don't miss out.")
    blog_title = models.CharField(max_length=100, default="LATEST NEWS & BLOGS")
    blog_subtitle = models.CharField(max_length=200, default="Voices of MYP")
    partners_title = models.CharField(max_length=100, default="PARTNERS & SPONSORS")
    
    # Link Texts
    view_all_departments_text = models.CharField(max_length=50, default="View all →")
    explore_projects_text = models.CharField(max_length=50, default="Explore projects")
    view_calendar_text = models.CharField(max_length=50, default="View calendar")
    all_articles_text = models.CharField(max_length=50, default="All articles →")
    
    # Testimonial
    testimonial_text = models.TextField(default="MYP gave me a community of mentors and a platform to launch my agribusiness. Today we employ 14 young people in Meru.")
    testimonial_author = models.CharField(max_length=100, default="Wanjiru K.")
    testimonial_role = models.CharField(max_length=100, default="MYP Member since 2022")
    
    # CTA Section
    cta_title = models.CharField(max_length=200, default="Ready to make an impact?")
    cta_subtitle = models.CharField(max_length=300, default="Join 1,200+ young professionals transforming Kenya — one project, one community at a time.")
    cta_button_text = models.CharField(max_length=50, default="Become a Member")
    cta_button_url = models.CharField(max_length=200, default="/members/register/")
    contact_button_text = models.CharField(max_length=50, default="Contact Us")
    contact_button_url = models.CharField(max_length=200, default="/contact/")
    
    # Footer
    footer_about = models.TextField(default="Empowering Professionals, Transforming Communities across the Mt. Kenya region and beyond.")
    footer_explore_title = models.CharField(max_length=50, default="EXPLORE")
    footer_engage_title = models.CharField(max_length=50, default="ENGAGE")
    footer_contact_title = models.CharField(max_length=50, default="CONTACT")
    footer_address = models.CharField(max_length=200, default="Meru Town, Kenya")
    footer_email = models.EmailField(default="info@myp.or.ke")
    footer_phone = models.CharField(max_length=50, default="+254 700 000 000")
    footer_copyright = models.CharField(max_length=200, default="2026 Meru Young Professionals. All rights reserved.")
    footer_tagline = models.CharField(max_length=200, default="Non-political · Non-profit · Youth-Led")
    
    # Colors
    primary_color = models.CharField(max_length=20, default="#0A7D3B", help_text="Primary brand color")
    secondary_color = models.CharField(max_length=20, default="#D32F2F", help_text="Secondary brand color")
    dark_color = models.CharField(max_length=20, default="#1A1A1A", help_text="Dark color for backgrounds")
    
    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"
    
    def __str__(self):
        return "Site Configuration"
    
    def save(self, *args, **kwargs):
        if not self.pk and SiteConfiguration.objects.exists():
            raise ValueError("Only one SiteConfiguration allowed. Edit existing one.")
        super().save(*args, **kwargs)


class Stat(models.Model):
    """Statistics - Members, Departments, Projects, Communities"""
    label = models.CharField(max_length=50, help_text="e.g., MEMBERS, DEPARTMENTS")
    value = models.CharField(max_length=50, help_text="e.g., 1,200+, 8+")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.label}: {self.value}"


class CoreValue(models.Model):
    """Core values - Hand-coded as per screenshot: Integrity, Accountability, etc."""
    title = models.CharField(max_length=50)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title


class Department(models.Model):
    """Departments - Admin adds these"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(default="Specialized programmes, mentorship and projects led by member experts.")
    icon = models.CharField(max_length=50, help_text="FontAwesome icon (e.g., fa-crown, fa-chart-line)")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """Projects - Admin adds these"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    status = models.CharField(max_length=50, default="Ongoing")
    location = models.CharField(max_length=200, default="Multiple counties")
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title


class Event(models.Model):
    """Events - Admin adds these"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    date = models.CharField(max_length=50, help_text="e.g., 12 Jul • Meru")
    venue = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=50, default="fa-calendar-alt")
    registration_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title


class BlogPost(models.Model):
    """Blog posts - Admin adds these"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField()
    content = RichTextUploadingField()
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    category = models.CharField(max_length=100, default="Leadership")
    published_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title


class Partner(models.Model):
    """Partners - Admin adds these with logos"""
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='partners/', blank=True, null=True)
    website = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name


class Leader(models.Model):
    """Leadership team - Admin adds these"""
    CATEGORY_CHOICES = (
        ('council', 'Executive Council'),
        ('department', 'Department Leadership'),
    )
    
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='council')
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='leadership/', blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.name} - {self.title}"


class GalleryImage(models.Model):
    """Gallery images - Admin adds these"""
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title


class Constitution(models.Model):
    """Constitution document - Admin uploads PDF"""
    title = models.CharField(max_length=200, default="MYP Constitution")
    version = models.CharField(max_length=20, default="1.0")
    content = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='constitution/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Constitution"
    
    def __str__(self):
        return f"{self.title} v{self.version}"


class Announcement(models.Model):
    """Announcement bar - Admin adds this"""
    message = models.CharField(max_length=500)
    link = models.URLField(blank=True)
    link_text = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.message[:50]
