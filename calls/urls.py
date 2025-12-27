"""
URL configuration for Twilio webhooks.
"""
from django.urls import path
from . import views

app_name = 'calls'

urlpatterns = [
    # Twilio webhooks
    path('call-status/', views.call_status_webhook, name='call-status'),
    path('recording-status/', views.recording_status_webhook, name='recording-status'),
    path('incoming-call/', views.incoming_call_webhook, name='incoming-call'),
    path('voice/', views.voice_webhook, name='voice'),
]
