"""
Diagnostic and Fix Script for Twilio CRM
Run this to check everything and create test users
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twilio_crm.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

print("="*60)
print("TWILIO CRM DIAGNOSTIC REPORT")
print("="*60)

# 1. Check Environment Variables
print("\n1. ENVIRONMENT VARIABLES:")
print(f"   TWILIO_ACCOUNT_SID: {'✓ SET' if settings.TWILIO_ACCOUNT_SID else '✗ MISSING'}")
print(f"   TWILIO_AUTH_TOKEN: {'✓ SET' if settings.TWILIO_AUTH_TOKEN else '✗ MISSING'}")
print(f"   TWILIO_PHONE_NUMBER: {settings.TWILIO_PHONE_NUMBER or '✗ MISSING'}")
print(f"   TWILIO_APP_SID: {settings.TWILIO_APP_SID or '✗ MISSING'}")
print(f"   TWILIO_API_KEY_SID: {settings.TWILIO_API_KEY_SID or '✗ MISSING (REQUIRED!)'}")
print(f"   TWILIO_API_KEY_SECRET: {'✓ SET' if settings.TWILIO_API_KEY_SECRET else '✗ MISSING (REQUIRED!)'}")

# 2. Check Users
print("\n2. USER ACCOUNTS:")
users_to_check = ['admin', 'agent1', 'agent2', 'manager1']
for username in users_to_check:
    user = User.objects.filter(username=username).first()
    if user:
        print(f"   ✓ {username:15} - Role: {user.role:10} - Active: {user.is_active}")
    else:
        print(f"   ✗ {username:15} - NOT FOUND")

# 3. Create Missing Users
print("\n3. CREATING MISSING TEST USERS:")
users_to_create = [
    {'username': 'admin', 'password': 'admin123', 'email': 'admin@example.com', 'role': 'agent', 'is_staff': True, 'is_superuser': True},
    {'username': 'agent1', 'password': 'test123', 'email': 'agent1@example.com', 'first_name': 'John', 'last_name': 'Agent', 'role': 'agent'},
    {'username': 'agent2', 'password': 'test123', 'email': 'agent2@example.com', 'first_name': 'Jane', 'last_name': 'Agent', 'role': 'agent'},
    {'username': 'manager1', 'password': 'test123', 'email': 'manager1@example.com', 'first_name': 'Mike', 'last_name': 'Manager', 'role': 'manager'},
]

for user_data in users_to_create:
    username = user_data['username']
    if not User.objects.filter(username=username).exists():
        password = user_data.pop('password')
        is_superuser = user_data.pop('is_superuser', False)

        if is_superuser:
            user = User.objects.create_superuser(username=username, password=password, **user_data)
        else:
            user = User.objects.create_user(username=username, password=password, **user_data)

        print(f"   ✓ Created: {username} (password: {password})")
    else:
        print(f"   ℹ Exists: {username}")

# 4. Test Token Generation
print("\n4. TESTING TOKEN GENERATION:")
try:
    from calls.services import twilio_service

    # Test with a dummy identity
    test_identity = "test_user_123"

    print(f"   Attempting to generate token for identity: {test_identity}")

    # Check what signing method will be used
    if settings.TWILIO_API_KEY_SID and settings.TWILIO_API_KEY_SECRET:
        print(f"   ✓ Will use API Key: {settings.TWILIO_API_KEY_SID[:10]}...")
    else:
        print(f"   ⚠ Will use Account SID (NOT RECOMMENDED)")

    token = twilio_service.generate_access_token(test_identity)

    print(f"   ✓ Token generated successfully!")
    print(f"   Token preview: {token[:50]}...")
    print(f"   Token length: {len(token)} characters")

except Exception as e:
    print(f"   ✗ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

# 5. Summary
print("\n" + "="*60)
print("SUMMARY:")
print("="*60)

if not settings.TWILIO_API_KEY_SID or not settings.TWILIO_API_KEY_SECRET:
    print("\n⚠️  WARNING: TWILIO API KEYS NOT CONFIGURED!")
    print("\nTO FIX:")
    print("1. Go to: https://console.twilio.com/us1/account/keys-credentials/api-keys")
    print("2. Create a new API Key")
    print("3. Add to your .env file:")
    print("   TWILIO_API_KEY_SID=SKxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print("   TWILIO_API_KEY_SECRET=your_secret_here")
    print("4. Restart the server")
else:
    print("\n✓ All environment variables are configured!")
    print("\nYou can now:")
    print("1. Start server: python manage.py runserver 0.0.0.0:8000")
    print("2. Open: http://localhost:8000/agent_call_client.html")
    print("3. Login: agent1 / test123")

print("\n" + "="*60)
