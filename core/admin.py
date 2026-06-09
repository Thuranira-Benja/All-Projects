from django.contrib import admin
from .models import (
    SiteConfiguration, Stat, CoreValue, Department, Project, Event,
    BlogPost, Partner, Leader, GalleryImage, Constitution, Announcement
)

class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(SingletonAdmin):
    fieldsets = (
        ('Logo & Branding', {'fields': ('logo', 'logo_footer', 'favicon', 'primary_color', 'secondary_color', 'dark_color')}),
        ('Hero Section', {'fields': ('hero_type', 'hero_background', 'hero_video', 'hero_tagline', 'hero_title_line1', 'hero_title_line2', 'hero_title_line3', 'hero_subtitle')}),
        ('Buttons', {'fields': ('become_member_text', 'become_member_url', 'join_us_text', 'join_us_url')}),
        ('Welcome Section', {'fields': ('welcome_title', 'welcome_content', 'learn_more_url')}),
        ('Cards Content', {'fields': ('mission_text', 'vision_text', 'community_text', 'innovation_text')}),
        ('Section Titles', {'fields': ('core_values_title', 'core_values_subtitle', 'departments_title', 'departments_subtitle', 'projects_title', 'projects_subtitle', 'events_title', 'events_subtitle', 'blog_title', 'blog_subtitle', 'partners_title')}),
        ('Link Texts', {'fields': ('view_all_departments_text', 'explore_projects_text', 'view_calendar_text', 'all_articles_text')}),
        ('Testimonial', {'fields': ('testimonial_text', 'testimonial_author', 'testimonial_role')}),
        ('CTA Section', {'fields': ('cta_title', 'cta_subtitle', 'cta_button_text', 'cta_button_url', 'contact_button_text', 'contact_button_url')}),
        ('Footer', {'fields': ('footer_about', 'footer_explore_title', 'footer_engage_title', 'footer_contact_title', 'footer_address', 'footer_email', 'footer_phone', 'footer_copyright', 'footer_tagline')}),
    )

@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'order', 'is_active')
    list_editable = ('order', 'is_active')

@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'location', 'order', 'is_featured')
    list_editable = ('order', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'order', 'is_featured')
    list_editable = ('order', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_date', 'is_published')
    list_filter = ('category', 'is_published')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_editable = ('order', 'is_active')

@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'category', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('category', 'is_active')

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

@admin.register(Constitution)
class ConstitutionAdmin(admin.ModelAdmin):
    list_display = ('title', 'version', 'is_active')
    list_editable = ('is_active',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('message', 'is_active', 'created_at')
    list_editable = ('is_active',)
