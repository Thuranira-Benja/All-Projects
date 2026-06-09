from django.urls import path
from . import views

app_name = 'leadership'

urlpatterns = [
    path('', views.leadership_view, name='leadership'),
]
