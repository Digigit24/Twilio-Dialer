# Quick Start Guide - 5 Minutes to Running

This guide will get you from zero to a running Twilio VoIP CRM in under 5 minutes.

---

## Step 1: Set Up Environment (1 minute)

```bash
# Navigate to project
cd Twilio-Dialer

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 2: Initialize Database (1 minute)

```bash
# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123 (or your choice)
```

---

## Step 3: Create Test Users (1 minute)

```bash
# Open Django shell
python manage.py shell
```

Paste this code:
```python
from accounts.models import User

# Create Agent
agent = User.objects.create_user(
    username='agent1',
    password='test123',
    email='agent1@example.com',
    first_name='John',
    last_name='Doe',
    role=User.Role.AGENT,
    phone_number='+1234567890',
    extension='101',
    is_available=True
)

# Create Manager
manager = User.objects.create_user(
    username='manager1',
    password='test123',
    email='manager1@example.com',
    first_name='Jane',
    last_name='Smith',
    role=User.Role.MANAGER,
    phone_number='+1234567891',
    extension='200'
)

print("✅ Users created successfully!")
print(f"Agent: {agent.username} / test123")
print(f"Manager: {manager.username} / test123")
exit()
```

---

## Step 4: Start Server (10 seconds)

```bash
# Start Django development server
python manage.py runserver
```

Server will start at: **http://localhost:8000**

---

## Step 5: Test the System (2 minutes)

### A. Access Admin Panel
1. Open: http://localhost:8000/admin
2. Login with admin credentials
3. Explore Users, Calls, Leads, Contacts

### B. View API Documentation
1. Open: http://localhost:8000/api/docs/
2. Browse all available endpoints
3. See request/response examples

### C. Test API

**1. Login as Agent:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "agent1", "password": "test123"}'
```

Copy the `access` token from response.

**2. Get User Profile:**
```bash
curl http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**3. Generate Twilio Token:**
```bash
curl -X POST http://localhost:8000/api/twilio/token/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**4. Create a Lead:**
```bash
curl -X POST http://localhost:8000/api/leads/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "Lead",
    "phone_number": "+1555123456",
    "email": "test@example.com",
    "company": "Test Corp",
    "status": "NEW"
  }'
```

**5. Get Statistics:**
```bash
curl http://localhost:8000/api/statistics/calls/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## ✅ You're Done!

Your Twilio VoIP CRM is now running locally!

---

## Next Steps

### To Enable Calling (Optional)

**1. Complete Twilio Setup:**
- Create TwiML App in Twilio Console
- Add App SID to `.env`
- Configure phone number

**2. Expose Webhooks:**
```bash
# Install ngrok
brew install ngrok

# Start ngrok
ngrok http 8000

# Copy the https URL (e.g., https://abc123.ngrok.io)
```

**3. Update Twilio Webhooks:**
- Voice URL: `https://abc123.ngrok.io/webhooks/voice/`
- Status Callback: `https://abc123.ngrok.io/webhooks/call-status/`
- Incoming Call: `https://abc123.ngrok.io/webhooks/incoming-call/`

**4. Update Django ALLOWED_HOSTS:**
Edit `.env`:
```env
ALLOWED_HOSTS=localhost,127.0.0.1,abc123.ngrok.io
```

Restart server.

**5. Test Making a Call:**
```bash
curl -X POST http://localhost:8000/api/calls/initiate/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to_number": "+1555123456",
    "record": true
  }'
```

---

## Useful URLs

| Resource | URL |
|----------|-----|
| Admin Panel | http://localhost:8000/admin |
| API Documentation | http://localhost:8000/api/docs/ |
| ReDoc | http://localhost:8000/api/redoc/ |
| API Base | http://localhost:8000/api/ |

---

## Test Credentials

| User | Username | Password | Role |
|------|----------|----------|------|
| Admin | admin | admin123 | Admin |
| Agent | agent1 | test123 | Agent |
| Manager | manager1 | test123 | Manager |

---

## Common Commands

```bash
# Start server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Make migrations
python manage.py makemigrations
python manage.py migrate

# Open shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

---

## Troubleshooting

**Problem: Module not found**
```bash
pip install -r requirements.txt
```

**Problem: Database locked**
```bash
# Delete db.sqlite3 and recreate
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

**Problem: Port already in use**
```bash
# Use different port
python manage.py runserver 8080
```

---

## Need Help?

- See `docs/SETUP_GUIDE.md` for detailed instructions
- See `docs/API_DOCUMENTATION.md` for API reference
- See `PROJECT_SUMMARY.md` for overview
- See `CREDENTIALS.md` for Twilio credentials

---

**You're all set! Start building your frontend or test the API!** 🚀
