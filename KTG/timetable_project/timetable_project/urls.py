from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('timetable.urls')),  # Root is handled by the timetable app
    path('accounts/', include('django.contrib.auth.urls')),  # For login/logout
]
