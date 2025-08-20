from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessPermitViewSet, dashboard_view

router = DefaultRouter()
router.register(r'business-permits', BusinessPermitViewSet, basename='business-permits')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', dashboard_view, name='dashboard'),
]
