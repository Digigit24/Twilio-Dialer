#!/usr/bin/env python
"""
Seed script to create initial users for Twilio CRM.
Run with: python seed_users.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twilio_crm.settings')
django.setup()

from accounts.models import User


def seed_users():
    """Create default users if they don't exist."""

    users_to_create = [
        {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'admin123',
            'role': User.Role.ADMIN,
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
        },
        {
            'username': 'manager1',
            'email': 'manager1@example.com',
            'password': 'test123',
            'role': User.Role.MANAGER,
            'first_name': 'Manager',
            'last_name': 'One',
            'is_staff': True,
        },
        {
            'username': 'agent1',
            'email': 'agent1@example.com',
            'password': 'test123',
            'role': User.Role.AGENT,
            'first_name': 'Agent',
            'last_name': 'One',
        },
        {
            'username': 'agent2',
            'email': 'agent2@example.com',
            'password': 'test123',
            'role': User.Role.AGENT,
            'first_name': 'Agent',
            'last_name': 'Two',
        },
    ]

    created_count = 0
    updated_count = 0

    for user_data in users_to_create:
        username = user_data.pop('username')
        password = user_data.pop('password')

        user, created = User.objects.get_or_create(
            username=username,
            defaults=user_data
        )

        if created:
            user.set_password(password)
            user.save()
            created_count += 1
            print(f"✅ Created user: {username} (role: {user.role})")
        else:
            # Update existing user
            for key, value in user_data.items():
                setattr(user, key, value)
            user.set_password(password)
            user.save()
            updated_count += 1
            print(f"🔄 Updated user: {username} (role: {user.role})")

    print(f"\n✅ Seed complete: {created_count} created, {updated_count} updated")
    print("\nYou can now login with:")
    print("  - Username: agent1, Password: test123 (Agent)")
    print("  - Username: manager1, Password: test123 (Manager)")
    print("  - Username: admin, Password: admin123 (Admin)")


if __name__ == '__main__':
    seed_users()
