from django.urls import path
from . import views

app_name = 'membership'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('success/', views.success, name='success'),
]
