"""
Admin configuration for calls app.
"""
from django.contrib import admin
from .models import Lead, Contact, Call, CallRecording


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'company', 'phone_number', 'status', 'assigned_to', 'created_at']
    list_filter = ['status', 'assigned_to', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number', 'company']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Company Information', {
            'fields': ('company',)
        }),
        ('Lead Status', {
            'fields': ('status', 'assigned_to')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'company', 'phone_number', 'position', 'assigned_to', 'created_at']
    list_filter = ['assigned_to', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number', 'company', 'position']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Company Information', {
            'fields': ('company', 'position')
        }),
        ('Assignment', {
            'fields': ('assigned_to',)
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = [
        'call_sid', 'direction', 'status', 'from_number', 'to_number',
        'agent', 'duration', 'start_time', 'created_at'
    ]
    list_filter = ['direction', 'status', 'agent', 'created_at']
    search_fields = ['call_sid', 'from_number', 'to_number', 'agent__username']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    readonly_fields = ['call_sid', 'parent_call_sid', 'created_at', 'updated_at']

    fieldsets = (
        ('Twilio Information', {
            'fields': ('call_sid', 'parent_call_sid')
        }),
        ('Call Details', {
            'fields': ('direction', 'status', 'from_number', 'to_number')
        }),
        ('Assignment', {
            'fields': ('agent', 'lead', 'contact')
        }),
        ('Metrics', {
            'fields': ('duration', 'start_time', 'end_time')
        }),
        ('Additional Information', {
            'fields': ('call_notes', 'tags')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CallRecording)
class CallRecordingAdmin(admin.ModelAdmin):
    list_display = [
        'recording_sid', 'call', 'status', 'duration',
        'file_size', 'is_transcribed', 'created_at'
    ]
    list_filter = ['status', 'is_transcribed', 'created_at']
    search_fields = ['recording_sid', 'call__call_sid']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    readonly_fields = ['recording_sid', 'recording_url', 'created_at', 'updated_at']

    fieldsets = (
        ('Twilio Information', {
            'fields': ('recording_sid', 'recording_url', 'call')
        }),
        ('Recording Details', {
            'fields': ('status', 'duration', 'file_size', 'local_file')
        }),
        ('Transcription', {
            'fields': ('is_transcribed', 'transcription')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
