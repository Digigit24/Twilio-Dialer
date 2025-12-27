"""
URL configuration for API endpoints.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = 'api'

# Create router and register viewsets
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'leads', views.LeadViewSet, basename='lead')
router.register(r'contacts', views.ContactViewSet, basename='contact')
router.register(r'calls', views.CallViewSet, basename='call')
router.register(r'recordings', views.CallRecordingViewSet, basename='recording')

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Twilio token generation
    path('twilio/token/', views.generate_access_token, name='twilio_token'),

    # Statistics endpoints
    path('statistics/calls/', views.call_statistics, name='call_statistics'),
    path('statistics/agents/', views.agent_statistics, name='agent_statistics'),

    # Include router URLs
    path('', include(router.urls)),
]
