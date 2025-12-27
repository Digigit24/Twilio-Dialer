@echo off
echo Fixing twilio_crm\urls.py merge conflict...

(
echo """
echo URL configuration for twilio_crm project.
echo """
echo from django.contrib import admin
echo from django.urls import path, include
echo from django.conf import settings
echo from django.conf.urls.static import static
echo from django.views.generic import TemplateView
echo from rest_framework import permissions
echo from drf_yasg.views import get_schema_view
echo from drf_yasg import openapi
echo from api.client_views import agent_call_client
echo.
echo # API Documentation
echo schema_view = get_schema_view^(
echo     openapi.Info^(
echo         title="Twilio CRM API",
echo         default_version='v1',
echo         description="API documentation for Twilio VoIP ^& WebRTC CRM System",
echo         terms_of_service="https://www.example.com/terms/",
echo         contact=openapi.Contact^(email="contact@example.com"^),
echo         license=openapi.License^(name="BSD License"^),
echo     ^),
echo     public=True,
echo     permission_classes=[permissions.AllowAny],
echo ^)
echo.
echo urlpatterns = [
echo     path^('admin/', admin.site.urls^),
echo.
echo     # Client Applications
echo     path^('', agent_call_client, name='home'^),
echo     path^('agent_call_client.html', agent_call_client, name='agent_call_client'^),
echo.
echo     # API Documentation
echo     path^('api/docs/', schema_view.with_ui^('swagger', cache_timeout=0^), name='schema-swagger-ui'^),
echo     path^('api/redoc/', schema_view.with_ui^('redoc', cache_timeout=0^), name='schema-redoc'^),
echo.
echo     # API endpoints
echo     path^('api/', include^('api.urls'^)^),
echo.
echo     # Webhooks
echo     path^('webhooks/', include^('calls.urls'^)^),
echo ]
echo.
echo # Serve media files in development
echo if settings.DEBUG:
echo     urlpatterns += static^(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT^)
echo     urlpatterns += static^(settings.STATIC_URL, document_root=settings.STATIC_ROOT^)
) > twilio_crm\urls.py

echo.
echo ✓ File fixed! Now run: python manage.py runserver 0.0.0.0:8000
pause
