from django.urls import path
from . import views

app_name = 'constitution'

urlpatterns = [
    path('', views.constitution_view, name='constitution'),
]
