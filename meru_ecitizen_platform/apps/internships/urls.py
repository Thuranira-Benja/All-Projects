from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InternshipViewSet, InternshipApplicationViewSet

router = DefaultRouter()
router.register(r'internships', InternshipViewSet, basename='internships')
router.register(r'applications', InternshipApplicationViewSet, basename='internship-applications')

urlpatterns = [
    path('', include(router.urls)),
]
