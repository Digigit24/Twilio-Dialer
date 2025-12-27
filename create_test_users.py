#!/usr/bin/env python
"""
Script to create test users for Twilio CRM.
Run this after running migrations.

Usage:
    python create_test_users.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twilio_crm.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()


def create_test_users():
    """Create test users for development."""

    print("=" * 60)
    print("Creating Test Users for Twilio CRM")
    print("=" * 60)

    # Create superuser
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@example.com',
            first_name='Admin',
            last_name='User'
        )
        print(f"✅ Created superuser: {admin.username} (password: admin123)")
    else:
        print("ℹ️  Superuser 'admin' already exists")

    # Create agent users
    agents = [
        {'username': 'agent1', 'password': 'test123', 'first_name': 'John', 'last_name': 'Agent'},
        {'username': 'agent2', 'password': 'test123', 'first_name': 'Jane', 'last_name': 'Agent'},
    ]

    for agent_data in agents:
        if not User.objects.filter(username=agent_data['username']).exists():
            agent = User.objects.create_user(
                username=agent_data['username'],
                password=agent_data['password'],
                email=f"{agent_data['username']}@example.com",
                first_name=agent_data['first_name'],
                last_name=agent_data['last_name'],
                role='agent'
            )
            print(f"✅ Created agent: {agent.username} (password: {agent_data['password']})")
        else:
            print(f"ℹ️  Agent '{agent_data['username']}' already exists")

    # Create manager users
    managers = [
        {'username': 'manager1', 'password': 'test123', 'first_name': 'Mike', 'last_name': 'Manager'},
    ]

    for manager_data in managers:
        if not User.objects.filter(username=manager_data['username']).exists():
            manager = User.objects.create_user(
                username=manager_data['username'],
                password=manager_data['password'],
                email=f"{manager_data['username']}@example.com",
                first_name=manager_data['first_name'],
                last_name=manager_data['last_name'],
                role='manager'
            )
            print(f"✅ Created manager: {manager.username} (password: {manager_data['password']})")
        else:
            print(f"ℹ️  Manager '{manager_data['username']}' already exists")

    print("\n" + "=" * 60)
    print("Test Users Created Successfully!")
    print("=" * 60)
    print("\nYou can now login with:")
    print("  - Admin:    username='admin'    password='admin123'")
    print("  - Agent:    username='agent1'   password='test123'")
    print("  - Agent:    username='agent2'   password='test123'")
    print("  - Manager:  username='manager1' password='test123'")
    print("\nNext steps:")
    print("  1. Start the server: python manage.py runserver 0.0.0.0:8000")
    print("  2. Open browser: http://localhost:8000/agent_call_client.html")
    print("  3. Login with agent1/test123")
    print("  4. Make a test call!")
    print("=" * 60)


if __name__ == '__main__':
    create_test_users()
