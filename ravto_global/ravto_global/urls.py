from django.contrib import admin
from django.urls import path
from core import views as core_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('about/', core_views.about, name='about'),
    path('contact/', core_views.contact, name='contact'),
    path('services/', core_views.services_view, name='services'),
    path('request-service/', core_views.request_service, name='request_service'),

    # ADD THIS NEW PATH for service detail
    path('services/<int:service_id>/', core_views.service_detail, name='service_detail'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
