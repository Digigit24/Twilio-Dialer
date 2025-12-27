# 🚀 Complete Testing Guide - Windows

## ✅ All Issues Fixed!

Your Twilio CRM is now ready to test. Follow these steps to test calling from your browser.

---

## 📋 Prerequisites Checklist

Before starting, make sure you have:
- [x] Python installed
- [x] Virtual environment activated
- [x] All dependencies installed (`pip install -r requirements.txt`)
- [x] Database migrated (`python manage.py migrate`)
- [x] `.env` file with Twilio credentials (automatically created)

---

## 🎯 STEP 1: Start Django Server

Open **Command Prompt** or **PowerShell**:

```cmd
cd C:\path\to\Twilio-Dialer
venv\Scripts\activate
python manage.py runserver 0.0.0.0:8000
```

**Expected output:**
```
System check identified no issues (0 silenced).
Django version 4.2.9, using settings 'twilio_crm.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CTRL-BREAK.
```

✅ **Server is running!**

---

## 🌐 STEP 2: Open Browser Call Client

1. Open your browser (Chrome recommended)
2. Navigate to the project folder
3. Double-click: **`agent_call_client.html`**

   Or manually open: `file:///C:/path/to/Twilio-Dialer/agent_call_client.html`

**You should see:** A beautiful login page with "Twilio CRM Call Client"

---

## 🔐 STEP 3: Login to Call Client

In the browser page:

1. **Username:** `agent1` (already filled)
2. **Password:** `test123` (already filled)
3. Click **"Login & Connect"**

**What happens:**
1. ⏳ "Logging in..." appears
2. ⏳ "Getting Twilio token..." appears
3. ⏳ "Connecting to Twilio..." appears
4. ✅ "Ready! Connected as agent1" appears
5. Call interface shows up

---

## 📞 STEP 4: Make a Test Call

### Option A: Call Any Phone Number

1. Enter a phone number in the format: `+1234567890`
   - Example: `+15551234567`
   - Or your own mobile: `+1YOURNUMBER`

2. Click **"Make Call"**

3. **Expected:**
   - Status shows "Calling +1..."
   - Your phone rings! 🎉
   - Answer the call and you'll hear audio
   - Click "Hang Up" to end

### Option B: Test Incoming Calls (Advanced - Requires ngrok)

See "Advanced Testing" section below.

---

## 🧪 STEP 5: Test API Endpoints

### Test 1: Check API Documentation

Open browser: http://localhost:8000/api/docs/

You should see **Swagger UI** with all API endpoints!

### Test 2: Check Admin Panel

1. Open: http://localhost:8000/admin
2. Login:
   - **Username:** `admin`
   - **Password:** `admin123`
3. Click **Calls** to see call history
4. Click **Users** to see agents

### Test 3: Test API with curl

Open Command Prompt:

```cmd
REM Login
curl -X POST http://localhost:8000/api/auth/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\": \"agent1\", \"password\": \"test123\"}"

REM You'll get an access token - copy it!

REM Get user profile (replace YOUR_TOKEN)
curl http://localhost:8000/api/users/me/ ^
  -H "Authorization: Bearer YOUR_TOKEN"

REM Get Twilio token
curl -X POST http://localhost:8000/api/twilio/token/ ^
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📱 Advanced Testing: Incoming Calls

To test **incoming calls** (customers calling your Twilio number), you need ngrok:

### Step 1: Install ngrok

1. Download: https://ngrok.com/download
2. Extract `ngrok.exe`
3. Sign up at: https://dashboard.ngrok.com/signup
4. Get auth token: https://dashboard.ngrok.com/get-started/your-authtoken
5. Run:
   ```cmd
   ngrok config add-authtoken YOUR_TOKEN
   ```

### Step 2: Start ngrok

Open a **new Command Prompt**:

```cmd
cd C:\path\to\Twilio-Dialer
ngrok http 8000
```

**Copy the HTTPS URL** (like `https://abc123.ngrok.io`)

### Step 3: Update .env

Edit `.env` file:

```env
ALLOWED_HOSTS=localhost,127.0.0.1,abc123.ngrok.io
```

**Restart Django server** (Ctrl+C then `python manage.py runserver 0.0.0.0:8000`)

### Step 4: Configure Twilio

1. Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/incoming
2. Click on: **+17656456867**
3. Set:
   - **A CALL COMES IN:** `https://abc123.ngrok.io/webhooks/incoming-call/`
   - **CALL STATUS CHANGES:** `https://abc123.ngrok.io/webhooks/call-status/`
4. Click **Save**

### Step 5: Test Incoming Call

1. **Keep browser client open and logged in**
2. Call **+1-765-645-6867** from any phone
3. **Your browser client will ring!** 📞
4. Click "Answer" to accept the call
5. Talk through your browser!

---

## 🎨 Features of the Browser Client

### What You Can Do:

✅ **Login** - Authenticate with agent credentials
✅ **Make Calls** - Call any phone number
✅ **Receive Calls** - Answer incoming calls (with ngrok)
✅ **Real-time Status** - See connection status
✅ **Hang Up** - End calls anytime
✅ **Logout** - Disconnect and logout

### Visual Indicators:

- 🔵 **Blue** - Information messages
- 🟢 **Green** - Success (connected, call answered)
- 🔴 **Red** - Errors
- 🟡 **Yellow** - Warnings (incoming call)

---

## 🔍 Troubleshooting

### Issue 1: "Credentials are required" Error

**Solution:** 
- Make sure `.env` file exists in project root
- Check `.env` has your Twilio credentials
- Restart Django server

**Verify .env:**
```cmd
type .env
```

Should show:
```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+1XXXXXXXXXX
```

(Your actual credentials will be different)

### Issue 2: Browser Client Shows "Login Failed"

**Possible causes:**
1. Django server not running
2. Wrong username/password
3. CORS issue

**Solutions:**
- Check Django server is running on port 8000
- Use: `agent1` / `test123`
- Check browser console for errors (F12)

### Issue 3: "Failed to get Twilio token"

**Solution:**
- Check `.env` has correct Twilio credentials
- Restart Django server
- Check server logs for errors

### Issue 4: Call Doesn't Connect

**Possible causes:**
1. Invalid phone number format
2. Twilio account issues
3. No TwiML App configured

**Solutions:**
- Use format: `+1XXXXXXXXXX` (include country code)
- Check Twilio Console for account status
- For outbound calls, you may need to set up TwiML App (see below)

### Issue 5: Browser Asks for Microphone Permission

**This is normal!**
- Click **"Allow"** when browser asks for microphone
- This is required for WebRTC calls

---

## 🎯 Quick Test Scenarios

### Scenario 1: Basic API Test (No calling)
```
✅ Start Django server
✅ Open http://localhost:8000/api/docs/
✅ Try API endpoints
✅ Check admin panel
```

### Scenario 2: Browser Call Test
```
✅ Start Django server
✅ Open agent_call_client.html
✅ Login as agent1
✅ Enter phone number
✅ Make call
✅ Talk!
```

### Scenario 3: Full Incoming Call Test
```
✅ Start Django server
✅ Start ngrok
✅ Update .env with ngrok URL
✅ Configure Twilio webhooks
✅ Open browser client and login
✅ Call +17656456867 from phone
✅ Answer in browser
```

---

## 📊 What Gets Logged

Every call you make is automatically logged in the database!

**To view call logs:**
1. Go to: http://localhost:8000/admin
2. Login: `admin` / `admin123`
3. Click **Calls**

**You'll see:**
- Call SID
- Direction (incoming/outgoing)
- From/To numbers
- Agent assigned
- Duration
- Status
- Timestamp

---

## 🎓 Understanding the System

### How Outbound Calls Work:

```
Browser Client → Django API → Twilio → Phone Network → Recipient's Phone
```

1. You click "Make Call" in browser
2. Browser gets Twilio token from Django
3. Twilio connects your browser to the phone number
4. Call is logged in Django database

### How Incoming Calls Work (with ngrok):

```
Caller's Phone → Twilio → ngrok → Django → Browser Client
```

1. Someone calls +17656456867
2. Twilio asks Django: "What should I do?"
3. Django says: "Route to agent1's browser"
4. Your browser rings!

---

## 💡 Tips for Best Experience

1. **Use Chrome or Edge** - Best WebRTC support
2. **Allow microphone** - Required for calls
3. **Use headphones** - Prevents echo
4. **Stable internet** - Required for good call quality
5. **Keep browser tab active** - Don't minimize while on call

---

## 🆘 Need Help?

### Check Server Logs

In your Django terminal, look for errors:
```
INFO "POST /api/auth/login/ HTTP/1.1" 200
INFO "POST /api/twilio/token/ HTTP/1.1" 200
```

### Check Browser Console

Press **F12** in browser → **Console** tab
Look for any error messages

### Test Checklist

- [ ] Django server running on port 8000
- [ ] .env file exists with credentials
- [ ] Database migrated successfully
- [ ] Browser client opens without errors
- [ ] Login works (shows "Ready!")
- [ ] Can make outbound calls
- [ ] Calls are logged in admin panel

---

## ✅ Success Criteria

You know everything is working when:

✅ Django server starts without errors
✅ Browser client loads successfully  
✅ Login shows "Ready! Connected as agent1"
✅ Can make outbound calls to phone numbers
✅ Calls appear in admin panel
✅ API documentation accessible
✅ No errors in browser console

---

## 🚀 You're Ready!

**What you can do now:**
- Make calls from browser to any phone
- Track all calls in admin panel
- Use API for custom integrations
- Build mobile apps using the API

**Next steps:**
- Set up ngrok for incoming calls
- Build a React/Vue frontend
- Create Android/iOS apps
- Deploy to production

---

**Happy Calling! 📞**

For more details, see:
- `WINDOWS_SETUP.md` - Windows-specific setup
- `INCOMING_CALLS_SETUP.md` - Incoming calls configuration
- `docs/API_DOCUMENTATION.md` - Complete API reference
