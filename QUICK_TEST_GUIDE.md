# Quick Test Guide - Updated with Cookie Authentication

## 🚀 Quick Start (3 Steps)

### Step 1: Start Django Server
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Start server
python manage.py runserver 0.0.0.0:8000
```

**You should see:**
```
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```

### Step 2: Open Web Client
Open your browser and go to:
```
http://localhost:8000/
```

### Step 3: Login and Make a Call

**Login Credentials:**
- Username: `agent1`
- Password: `test123`

**Test Call:**
1. Click "Login & Connect"
2. Wait for "Ready!" message
3. Enter a phone number (e.g., +1234567890)
4. Click "Make Call"

✅ Done! You're now making VoIP calls from your browser!

---

## 🔧 What Changed?

### New Authentication System

**Before:**
- Manual token management in localStorage
- Had to include Bearer token in every request

**Now:**
- ✅ **Automatic cookie-based authentication**
- ✅ **Secure HttpOnly cookies**
- ✅ **CSRF protection built-in**
- ✅ **No manual token handling needed**

### New Features

1. **Cookie Authentication**: Tokens stored in secure HttpOnly cookies
2. **Multi-method Auth**: Supports cookies, Bearer tokens, and DRF tokens
3. **Auto Session Verification**: Checks if you're logged in on page load
4. **Better Error Messages**: Clear feedback on login issues

---

## 📝 Test Accounts

```
Agent:
  Username: agent1
  Password: test123
  Role: AGENT

Manager:
  Username: manager1
  Password: test123
  Role: MANAGER

Admin:
  Username: admin
  Password: admin123
  Role: ADMIN
```

---

## 🧪 Testing Checklist

### ✅ Basic Login Flow
- [ ] Open http://localhost:8000/
- [ ] Login with agent1/test123
- [ ] See "Ready! Connected as user_2 (agent1)"
- [ ] Check browser DevTools → Cookies
- [ ] Verify `access_token` and `refresh_token` cookies exist

### ✅ Make Outbound Call
- [ ] After login, enter phone number
- [ ] Click "Make Call"
- [ ] See "Calling..." then "Call connected!"
- [ ] Hang up button appears
- [ ] Click hang up

### ✅ Check Call Logs
- [ ] Go to http://localhost:8000/admin/
- [ ] Login with admin/admin123
- [ ] Click "Calls" → See your test call
- [ ] Verify call details are saved

### ✅ API Documentation
- [ ] Go to http://localhost:8000/api/docs/
- [ ] Browse available endpoints
- [ ] Try "Authorize" button
- [ ] Test API calls from Swagger UI

### ✅ Cookie Authentication
- [ ] Make a call successfully
- [ ] Refresh the page
- [ ] Click login again
- [ ] Should work without re-entering credentials (cookies still valid)

### ✅ Logout Flow
- [ ] Click "Logout" button
- [ ] See "Logged out successfully"
- [ ] Verify cookies are cleared (DevTools → Application → Cookies)
- [ ] Try to login again

---

## 🔍 Verify Authentication Works

### Test 1: Cookie-Based Auth
```bash
# Login and save cookies
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "agent1", "password": "test123"}' \
  -c cookies.txt

# Use cookies (no Bearer token needed!)
curl http://localhost:8000/api/auth/verify/ -b cookies.txt
```

**Expected:** User info returned ✅

### Test 2: Bearer Token (Fallback)
```bash
# Login
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "agent1", "password": "test123"}' \
  | jq -r '.access')

# Use Bearer token
curl http://localhost:8000/api/auth/verify/ \
  -H "Authorization: Bearer $TOKEN"
```

**Expected:** User info returned ✅

---

## 🐛 Troubleshooting

### Issue: Can't see the login page

**Solution:**
```bash
# Make sure server is running on correct port
python manage.py runserver 0.0.0.0:8000

# Open browser to exact URL
http://localhost:8000/
```

### Issue: "Invalid credentials" error

**Check:**
1. Username is `agent1` (lowercase)
2. Password is `test123` (exactly)
3. Check browser console for errors (F12)

**Fix:**
```bash
# Re-seed users
source venv/bin/activate
python seed_users.py
```

### Issue: Cookies not being set

**Solutions:**
1. Clear browser cookies (Settings → Privacy)
2. Try incognito/private window
3. Check DevTools console for CORS errors
4. Verify server URL is http://localhost:8000 (not 127.0.0.1)

### Issue: "Failed to get Twilio token"

**Check .env file:**
```bash
cat .env
```

**Should contain:**
```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

**Fix if missing:**
```bash
# Copy from .env.example
cp .env.example .env
# Then manually add your Twilio credentials
```

### Issue: Server won't start

**Error: "Address already in use"**
```bash
# Kill existing server
pkill -f "manage.py runserver"

# Wait 2 seconds, then start again
python manage.py runserver 0.0.0.0:8000
```

**Error: "No module named 'django'"**
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 📊 Success Indicators

When everything is working, you should see:

**Server Console:**
```
System check identified no issues (0 silenced).
December 27, 2025 - 11:35:00
Django version 4.2.9, using settings 'twilio_crm.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.

[27/Dec/2025 11:35:15] "POST /api/auth/login/ HTTP/1.1" 200 601
[27/Dec/2025 11:35:16] "POST /api/twilio/token/ HTTP/1.1" 200 123
```

**Browser Console:**
```
Login successful: {access: "eyJ...", user: {...}}
Device ready!
Call connected!
```

**Browser Cookies:**
```
access_token: eyJhbGc... (HttpOnly, 8 hours)
refresh_token: eyJhbGc... (HttpOnly, 7 days)
csrftoken: xyz123... (Session)
```

---

## 🎯 Next Steps

After successful testing:

1. **Configure Incoming Calls**: See WINDOWS_SETUP.md or INCOMING_CALLS_SETUP.md
2. **Explore API**: Visit http://localhost:8000/api/docs/
3. **Check Call Logs**: Admin panel at http://localhost:8000/admin/
4. **Build Mobile App**: Use the API endpoints
5. **Deploy to Production**: See deployment docs

---

## 📚 Additional Resources

- **Authentication Guide**: AUTHENTICATION_GUIDE.md
- **Full API Docs**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/
- **Incoming Calls Setup**: WINDOWS_SETUP.md

---

## ✅ All Tests Passed?

If you completed all checklist items:

🎉 **Congratulations!** Your Twilio CRM system is fully operational!

You now have:
- ✅ Cookie-based authentication working
- ✅ WebRTC calling from browser
- ✅ Call logging to database
- ✅ Multi-method auth (cookies + bearer + token)
- ✅ CSRF protection
- ✅ Secure HttpOnly cookies
- ✅ Full REST API ready for mobile apps

**Ready for production!** 🚀
