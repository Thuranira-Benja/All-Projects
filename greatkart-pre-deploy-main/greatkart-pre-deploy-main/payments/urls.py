from django.urls import path
from . import views

urlpatterns = [
    path('stk-push/', views.stk_push_payment, name='stk_push'),
]
