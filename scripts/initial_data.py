import os
import sys
import django

# Setup Django - use 'config.settings' not 'config.settings.base'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.models import SiteConfiguration, Stat, CoreValue, Partner
from apps.accounts.models import User
from apps.departments.models import Department

def load_initial_data():
    print("Loading initial data...")
    
    # Create site configuration
    config, created = SiteConfiguration.objects.get_or_create(
        id=1,
        defaults={
            'site_name': "Meru Young Professionals",
            'site_tagline': "Empowering Professionals, Transforming Communities",
            'hero_title': "Empowering Professionals, Transforming Communities",
            'hero_subtitle': "Meru Young Professionals unites a generation of leaders, innovators and changemakers from the Mt. Kenya region and beyond.",
            'about_content': "Meru Young Professionals (MYP) is a non-political, non-profit youth-led organization that brings together professionals from the Mt. Kenya region and beyond.",
            'mission_text': "To empower young professionals through leadership development, innovation, entrepreneurship, mentorship, community service, and sustainable growth.",
            'vision_text': "To become the leading network of transformative young professionals creating positive impact across Kenya and beyond.",
            'contact_email': "info@myporg.com",
            'contact_phone': "+254 700 000 000",
            'contact_address': "Meru, Kenya",
        }
    )
    print("✓ Site configuration created")
    
    # Create statistics
    stats_data = [
        {'label': 'Members', 'value': '1200+', 'icon': 'fa-users', 'order': 1},
        {'label': 'Departments', 'value': '8', 'icon': 'fa-building', 'order': 2},
        {'label': 'Projects', 'value': '45+', 'icon': 'fa-project-diagram', 'order': 3},
        {'label': 'Communities', 'value': '30+', 'icon': 'fa-globe', 'order': 4},
    ]
    
    for stat_data in stats_data:
        stat, created = Stat.objects.get_or_create(
            label=stat_data['label'],
            defaults=stat_data
        )
    print("✓ Statistics created")
    
    # Create core values
    values_data = [
        {'title': 'Integrity', 'icon': 'fa-shield-alt', 'description': 'Acting with honesty and transparency in all dealings.', 'order': 1},
        {'title': 'Accountability', 'icon': 'fa-check-circle', 'description': 'Taking responsibility for our actions and commitments.', 'order': 2},
        {'title': 'Excellence', 'icon': 'fa-star', 'description': 'Striving for the highest standards in everything we do.', 'order': 3},
        {'title': 'Innovation', 'icon': 'fa-lightbulb', 'description': 'Embracing new ideas and creative solutions.', 'order': 4},
        {'title': 'Teamwork', 'icon': 'fa-handshake', 'description': 'Working together to achieve greater impact.', 'order': 5},
        {'title': 'Professionalism', 'icon': 'fa-briefcase', 'description': 'Maintaining high professional standards.', 'order': 6},
        {'title': 'Service', 'icon': 'fa-heart', 'description': 'Dedicating ourselves to community service.', 'order': 7},
        {'title': 'Inclusivity', 'icon': 'fa-users', 'description': 'Welcoming all professionals regardless of background.', 'order': 8},
    ]
    
    for value_data in values_data:
        value, created = CoreValue.objects.get_or_create(
            title=value_data['title'],
            defaults=value_data
        )
    print("✓ Core values created")
    
    # Create departments
    departments_data = [
        {'name': 'Leadership & Governance', 'slug': 'leadership-governance', 'description': 'Specialized programmes, mentorship and projects led by member experts.', 'icon': 'fa-crown', 'leader_name': 'John Mwangi', 'leader_title': 'Chairperson', 'order': 1, 'is_active': True},
        {'name': 'Business & Entrepreneurship', 'slug': 'business-entrepreneurship', 'description': 'Specialized programmes, mentorship and projects led by member experts.', 'icon': 'fa-chart-line', 'leader_name': 'Jane Wanjiku', 'leader_title': 'Director', 'order': 2, 'is_active': True},
        {'name': 'Technology & Innovation', 'slug': 'technology-innovation', 'description': 'Specialized programmes, mentorship and projects led by member experts.', 'icon': 'fa-microchip', 'leader_name': 'Peter Kamau', 'leader_title': 'Lead', 'order': 3, 'is_active': True},
        {'name': 'Agriculture & Environment', 'slug': 'agriculture-environment', 'description': 'Specialized programmes, mentorship and projects led by member experts.', 'icon': 'fa-tree', 'leader_name': 'Mary Wambui', 'leader_title': 'Coordinator', 'order': 4, 'is_active': True},
        {'name': 'Education & Mentorship', 'slug': 'education-mentorship', 'description': 'Specialized programmes, mentorship and projects led by member experts.', 'icon': 'fa-graduation-cap', 'leader_name': 'James Otieno', 'leader_title': 'Director', 'order': 5, 'is_active': True},
        {'name': 'Finance & Investment', 'slug': 'finance-investment', 'description': 'Specialized programmes, mentorship and projects led by member experts.', 'icon': 'fa-coins', 'leader_name': 'Lucy Nderitu', 'leader_title': 'Treasurer', 'order': 6, 'is_active': True},
        {'name': 'Media & Communication', 'slug': 'media-communication', 'description': 'Specialized programmes, mentorship and projects led by member experts.', 'icon': 'fa-newspaper', 'leader_name': 'David Muthui', 'leader_title': 'Lead', 'order': 7, 'is_active': True},
        {'name': 'Community Development', 'slug': 'community-development', 'description': 'Specialized programmes, mentorship and projects led by member experts.', 'icon': 'fa-hand-holding-heart', 'leader_name': 'Esther Njeri', 'leader_title': 'Coordinator', 'order': 8, 'is_active': True},
    ]
    
    for dept_data in departments_data:
        department, created = Department.objects.get_or_create(
            slug=dept_data['slug'],
            defaults=dept_data
        )
    print("✓ Departments created")
    
    # Create partners
    partners_data = [
        {'name': 'County Government', 'logo': '', 'website': '#', 'order': 1},
        {'name': 'KEPSA', 'logo': '', 'website': '#', 'order': 2},
        {'name': 'UNDP', 'logo': '', 'website': '#', 'order': 3},
        {'name': 'Equity Bank', 'logo': '', 'website': '#', 'order': 4},
        {'name': 'Safaricom', 'logo': '', 'website': '#', 'order': 5},
        {'name': 'USAID', 'logo': '', 'website': '#', 'order': 6},
    ]
    
    for partner_data in partners_data:
        partner, created = Partner.objects.get_or_create(
            name=partner_data['name'],
            defaults=partner_data
        )
    print("✓ Partners created")
    
    # Create admin user
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@myporg.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            phone_number='+254700000000',
            is_approved=True
        )
        print("✓ Admin user created")
    
    print("\n✅ Initial data loaded successfully!")
    print("\nLogin credentials:")
    print("Username: admin")
    print("Password: admin123")

if __name__ == '__main__':
    load_initial_data()
