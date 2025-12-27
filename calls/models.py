"""
Models for call management and tracking.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone


class Lead(models.Model):
    """
    Lead/Prospect model for CRM.
    """
    class Status(models.TextChoices):
        NEW = 'NEW', 'New'
        CONTACTED = 'CONTACTED', 'Contacted'
        QUALIFIED = 'QUALIFIED', 'Qualified'
        CONVERTED = 'CONVERTED', 'Converted'
        LOST = 'LOST', 'Lost'

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    company = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads'
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company or 'No Company'}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class Contact(models.Model):
    """
    Contact model for converted leads/customers.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    company = models.CharField(max_length=200, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contacts'
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company or 'No Company'}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class Call(models.Model):
    """
    Call log model to track all calls.
    """
    class Direction(models.TextChoices):
        INBOUND = 'INBOUND', 'Incoming'
        OUTBOUND = 'OUTBOUND', 'Outgoing'

    class Status(models.TextChoices):
        INITIATED = 'INITIATED', 'Initiated'
        RINGING = 'RINGING', 'Ringing'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        BUSY = 'BUSY', 'Busy'
        FAILED = 'FAILED', 'Failed'
        NO_ANSWER = 'NO_ANSWER', 'No Answer'
        CANCELED = 'CANCELED', 'Canceled'

    # Twilio identifiers
    call_sid = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Twilio Call SID"
    )
    parent_call_sid = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Parent Call SID for transferred calls"
    )

    # Call details
    direction = models.CharField(
        max_length=10,
        choices=Direction.choices
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.INITIATED
    )

    # Participants
    from_number = models.CharField(max_length=20, help_text="Caller's phone number")
    to_number = models.CharField(max_length=20, help_text="Receiver's phone number")

    # Agent assignment
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='calls',
        help_text="Sales agent handling the call"
    )

    # Associated records
    lead = models.ForeignKey(
        Lead,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='calls',
        help_text="Associated lead"
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='calls',
        help_text="Associated contact"
    )

    # Call metrics
    duration = models.IntegerField(
        default=0,
        help_text="Call duration in seconds"
    )
    start_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Call start time"
    )
    end_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Call end time"
    )

    # Additional information
    call_notes = models.TextField(
        blank=True,
        null=True,
        help_text="Notes about the call"
    )
    tags = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Comma-separated tags"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Call'
        verbose_name_plural = 'Calls'
        indexes = [
            models.Index(fields=['call_sid']),
            models.Index(fields=['agent', '-created_at']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['direction', '-created_at']),
        ]

    def __str__(self):
        return f"{self.direction} call - {self.from_number} to {self.to_number} ({self.status})"

    def get_duration_formatted(self):
        """Return formatted duration (MM:SS)."""
        if self.duration:
            minutes = self.duration // 60
            seconds = self.duration % 60
            return f"{minutes:02d}:{seconds:02d}"
        return "00:00"


class CallRecording(models.Model):
    """
    Call recording model to store recording metadata.
    """
    class Status(models.TextChoices):
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'
        DELETED = 'DELETED', 'Deleted'

    # Associated call
    call = models.ForeignKey(
        Call,
        on_delete=models.CASCADE,
        related_name='recordings',
        help_text="Associated call"
    )

    # Twilio recording identifiers
    recording_sid = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Twilio Recording SID"
    )
    recording_url = models.URLField(
        max_length=500,
        help_text="Twilio recording URL"
    )

    # Recording details
    duration = models.IntegerField(
        default=0,
        help_text="Recording duration in seconds"
    )
    file_size = models.IntegerField(
        default=0,
        help_text="File size in bytes"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PROCESSING
    )

    # Local storage
    local_file = models.FileField(
        upload_to='recordings/',
        blank=True,
        null=True,
        help_text="Local copy of the recording"
    )

    # Access control
    is_transcribed = models.BooleanField(
        default=False,
        help_text="Whether the recording has been transcribed"
    )
    transcription = models.TextField(
        blank=True,
        null=True,
        help_text="Call transcription"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Call Recording'
        verbose_name_plural = 'Call Recordings'
        indexes = [
            models.Index(fields=['recording_sid']),
            models.Index(fields=['call', '-created_at']),
        ]

    def __str__(self):
        return f"Recording for {self.call.call_sid} ({self.status})"

    def get_duration_formatted(self):
        """Return formatted duration (MM:SS)."""
        if self.duration:
            minutes = self.duration // 60
            seconds = self.duration % 60
            return f"{minutes:02d}:{seconds:02d}"
        return "00:00"

    def get_file_size_formatted(self):
        """Return formatted file size."""
        if self.file_size:
            if self.file_size < 1024:
                return f"{self.file_size} B"
            elif self.file_size < 1024 * 1024:
                return f"{self.file_size / 1024:.2f} KB"
            else:
                return f"{self.file_size / (1024 * 1024):.2f} MB"
        return "0 B"
