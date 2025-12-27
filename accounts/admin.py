"""
Admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_available', 'is_active']
    list_filter = ['role', 'is_available', 'is_active', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']
    ordering = ['-date_joined']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('CRM Information', {
            'fields': ('role', 'phone_number', 'extension', 'is_available', 'twilio_client_identity')
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('CRM Information', {
            'fields': ('role', 'phone_number', 'extension', 'is_available')
        }),
    )
