from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('mission/', views.mission, name='mission'),
    path('leadership/', views.leadership, name='leadership'),
    path('leadership/apply/', views.leadership_apply, name='leadership_apply'),
    path('leadership/apply/submit/', views.leadership_apply_submit, name='leadership_apply_submit'),
    path('departments/', views.departments, name='departments'),
    path('departments/<slug:slug>/', views.department_detail, name='department_detail'),
    path('projects/', views.projects, name='projects'),
    path('events/', views.events, name='events'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('constitution/', views.constitution, name='constitution'),
    path('contact/', views.contact, name='contact'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('proposal/form/', views.proposal_form, name='proposal_form'),
    path('proposal/submit/', views.submit_proposal, name='submit_proposal'),
]
