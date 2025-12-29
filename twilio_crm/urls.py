"""
URL configuration for twilio_crm project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.client_views import agent_call_client

# API Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Twilio CRM API",
        default_version='v1',
        description="API documentation for Twilio VoIP & WebRTC CRM System",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Client Applications
    path('', agent_call_client, name='home'),
    path('agent_call_client.html', agent_call_client, name='agent_call_client'),
    
    # Test Config Page
    path('test_config.html', TemplateView.as_view(template_name='test_config.html'), name='test_config'),

    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # API endpoints
    path('api/', include('api.urls')),

    # Webhooks
    path('webhooks/', include('calls.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
