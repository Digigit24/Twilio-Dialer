"""
User models for the CRM system.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model with roles and additional fields.
    """
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        MANAGER = 'MANAGER', 'Manager'
        AGENT = 'AGENT', 'Sales Agent'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.AGENT,
        help_text="User role in the system"
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="User's contact phone number"
    )
    extension = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Internal extension number"
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Agent availability status for receiving calls"
    )
    twilio_client_identity = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        help_text="Unique Twilio client identity for WebRTC"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def is_agent(self):
        return self.role == self.Role.AGENT

    def is_manager(self):
        return self.role in [self.Role.MANAGER, self.Role.ADMIN]

    def is_admin(self):
        return self.role == self.Role.ADMIN
