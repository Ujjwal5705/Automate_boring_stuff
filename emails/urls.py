from django.urls import path
from . import views

urlpatterns = [
    path('send-emails/', views.send_emails, name='send_emails'),
]