from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BursaryApplicationViewSet, MpesaCallbackView

router = DefaultRouter()
router.register('', BursaryApplicationViewSet, basename='bursary-application')

urlpatterns = [
    path('', include(router.urls)),
    path('mpesa-callback/', MpesaCallbackView.as_view(), name='mpesa-callback'),
]