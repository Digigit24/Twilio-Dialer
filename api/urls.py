"""
URL configuration for API endpoints.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from . import auth_views

app_name = 'api'

# Create router and register viewsets
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'leads', views.LeadViewSet, basename='lead')
router.register(r'contacts', views.ContactViewSet, basename='contact')
router.register(r'calls', views.CallViewSet, basename='call')
router.register(r'recordings', views.CallRecordingViewSet, basename='recording')

urlpatterns = [
    # Authentication endpoints (Cookie-based with token fallback)
    path('auth/login/', auth_views.login_view, name='login'),
    path('auth/logout/', auth_views.logout_view, name='logout'),
    path('auth/refresh/', auth_views.refresh_token_view, name='token_refresh'),
    path('auth/verify/', auth_views.verify_token_view, name='verify_token'),

    # Twilio token generation
    path('twilio/token/', views.generate_access_token, name='twilio_token'),

    # Statistics endpoints
    path('statistics/calls/', views.call_statistics, name='call_statistics'),
    path('statistics/agents/', views.agent_statistics, name='agent_statistics'),

    # Include router URLs
    path('', include(router.urls)),
]
