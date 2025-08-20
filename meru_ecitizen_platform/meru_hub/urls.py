from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # API v1 Endpoints
    path('api/v1/bursary/', include('apps.bursary.urls')),
    path('api/v1/complaints/', include('apps.complaints.urls')),
    path('api/v1/licensing/', include('apps.licensing.urls')),
    path('api/v1/internships/', include('apps.internships.urls')),
    path('api/v1/agriculture/', include('apps.agriculture.urls')),
    path('api/v1/monitoring/', include('apps.monitoring.urls')),

    # JWT Authentication Endpoints
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
