# Twilio Dialer - Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- A Twilio account (sign up at https://www.twilio.com/try-twilio)
- Your Twilio credentials

---

## Step 1: Get Your Twilio Credentials

1. Go to https://console.twilio.com
2. Login or create a free account
3. From your Twilio Console Dashboard, copy:
   - **Account SID** (starts with AC...)
   - **Auth Token** (click to reveal)
4. Get a Twilio Phone Number:
   - Go to Phone Numbers → Manage → Buy a number
   - Choose a number with Voice capabilities
   - Copy the phone number (format: +1234567890)
5. Create a TwiML App:
   - Go to Voice → TwiML → TwiML Apps
   - Click "Create new TwiML App"
   - Name: "Twilio CRM App"
   - Voice Request URL: `http://your-server-url/webhooks/voice/` (for now use a placeholder)
   - Copy the App SID (starts with AP...)

---

## Step 2: Configure Environment Variables

1. Open the `.env` file in the project root
2. Replace the placeholder values with your actual Twilio credentials:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_actual_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
TWILIO_APP_SID=APxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**IMPORTANT**: These are REAL credentials from your Twilio account!

---

## Step 3: Install Dependencies

```bash
# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install/Update dependencies
pip install -r requirements.txt
```

---

## Step 4: Set Up Database

```bash
# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: (choose a password)

# Create test users for calling
python manage.py shell
```

In the Django shell, run:
```python
from django.contrib.auth import get_user_model
User = get_user_model()

# Create an agent user
agent = User.objects.create_user(
    username='agent1',
    password='test123',
    email='agent1@example.com',
    first_name='Test',
    last_name='Agent',
    role='agent'
)
print(f"Created agent: {agent.username}")

# Create a manager user
manager = User.objects.create_user(
    username='manager1',
    password='test123',
    email='manager1@example.com',
    first_name='Test',
    last_name='Manager',
    role='manager'
)
print(f"Created manager: {manager.username}")

exit()
```

---

## Step 5: Start the Server

```bash
python manage.py runserver 0.0.0.0:8000
```

You should see:
```
Starting development server at http://0.0.0.0:8000/
Quit the server with CTRL-BREAK.
```

**No errors should appear!** If you see the pkg_resources warning, that's just a deprecation warning and won't affect functionality.

---

## Step 6: Test in Browser

### Option A: Use the Browser Call Client

1. Open your browser to: **http://localhost:8000/agent_call_client.html**

2. Login with test credentials:
   - Username: `agent1`
   - Password: `test123`

3. You should see "✅ Ready! Connected as user_X"

4. Enter a phone number (format: +1234567890) and click "Make Call"

5. The call will go through Twilio to the destination number!

### Option B: Use the API Directly

1. Get an authentication token:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"agent1","password":"test123"}'
```

You'll get a response like:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

2. Make a call using the API:
```bash
curl -X POST http://localhost:8000/api/calls/initiate/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to_number": "+1234567890",
    "record": true
  }'
```

---

## Step 7: Access Admin Panel

1. Go to: **http://localhost:8000/admin/**
2. Login with superuser credentials
3. You can manage:
   - Users
   - Calls
   - Call Recordings
   - Leads
   - Contacts

---

## Troubleshooting

### Error: "Credentials are required to create a TwilioClient"
- Make sure you've set the correct values in `.env`
- Restart the server after updating `.env`

### Error: "Unable to create record: The requested resource..."
- Check that your Twilio Account SID and Auth Token are correct
- Make sure your Twilio account is active (not suspended)

### pkg_resources deprecation warning
- This is just a warning from an older dependency
- It won't affect functionality
- The warning will go away after updating dependencies

### Call not connecting
- Make sure your Twilio phone number has Voice capabilities
- Check that you have credits in your Twilio account
- Verify the destination number is in E.164 format (+1234567890)

---

## API Endpoints

### Authentication
- `POST /api/auth/login/` - Login and get JWT token
- `POST /api/auth/register/` - Register new user

### Calls
- `GET /api/calls/` - List all calls
- `POST /api/calls/initiate/` - Initiate a new call
- `GET /api/calls/{id}/` - Get call details
- `GET /api/calls/{id}/recordings/` - Get call recordings

### Twilio
- `POST /api/twilio/token/` - Get Twilio access token for WebRTC

### Users
- `GET /api/users/me/` - Get current user profile
- `POST /api/users/{id}/set_availability/` - Update availability

### Statistics
- `GET /api/statistics/calls/` - Get call statistics
- `GET /api/statistics/agents/` - Get agent statistics (managers only)

---

## Testing Checklist

- [ ] Server starts without errors
- [ ] Can login to admin panel
- [ ] Can login to browser call client
- [ ] Browser client shows "Ready" status
- [ ] Can make a test call to your mobile phone
- [ ] Call connects successfully
- [ ] Can hang up the call
- [ ] Call appears in admin panel
- [ ] Can view call recordings (if enabled)

---

## Next Steps

1. **Set up ngrok for webhooks**: To receive incoming calls, you need a public URL
   ```bash
   ngrok http 8000
   ```
   Then update your TwiML App Voice URL to: `https://your-ngrok-url.ngrok.io/webhooks/voice/`

2. **Add leads and contacts**: Go to admin panel and add test data

3. **Customize the call flow**: Edit `calls/services.py` to modify TwiML responses

4. **Set up production deployment**: Use gunicorn, nginx, and a proper database

---

## Need Help?

- Check Twilio Console logs: https://console.twilio.com/monitor/logs/calls
- Check Django logs in the terminal
- Verify your `.env` file has correct credentials
- Make sure you have Twilio credits

---

## Quick Commands Reference

```bash
# Start server
python manage.py runserver 0.0.0.0:8000

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Open Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```
