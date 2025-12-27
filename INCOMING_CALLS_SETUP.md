# 📞 Setting Up Incoming Calls - Complete Guide

## Problem
When someone calls your Twilio number (+17656456867), they hear "invalid number" because the number isn't configured to handle incoming calls yet.

## Solution
Set up webhooks so incoming calls are routed to your Django backend, which then routes them to available agents.

---

## 🚀 Quick Setup (10 Minutes)

### Step 1: Install ngrok (Expose Local Server)

Your Django server is running on localhost, but Twilio needs a public URL to send webhooks.

**Install ngrok:**
```bash
# macOS
brew install ngrok

# Linux
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar xvzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin

# Windows
# Download from https://ngrok.com/download
```

**Sign up for ngrok (free):**
1. Go to: https://dashboard.ngrok.com/signup
2. Sign up for a free account
3. Get your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken

**Configure ngrok:**
```bash
ngrok config add-authtoken YOUR_AUTHTOKEN
```

### Step 2: Start ngrok

```bash
# Start ngrok to expose port 8000
ngrok http 8000
```

**You'll see output like this:**
```
ngrok                                                           

Session Status                online
Account                       your-email@example.com
Version                       3.x.x
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok.io -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)

---

### Step 3: Update Django Settings

Edit your `.env` file to allow the ngrok domain:

```bash
nano .env
```

Update the `ALLOWED_HOSTS` line:
```env
ALLOWED_HOSTS=localhost,127.0.0.1,abc123.ngrok.io
```

**Important:** Replace `abc123.ngrok.io` with YOUR actual ngrok URL (without https://)

**Restart Django server:**
```bash
# Stop the current server (Ctrl+C or kill the process)
pkill -f "python manage.py runserver"

# Restart with ngrok domain allowed
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

---

### Step 4: Configure Twilio Phone Number

Now configure your Twilio number to route incoming calls to your Django backend.

**A. Go to Twilio Phone Numbers:**
https://console.twilio.com/us1/develop/phone-numbers/manage/incoming

**B. Click on your phone number:** +17656456867

**C. Scroll to "Voice Configuration" section**

**D. Configure as follows:**
```
Configure with: Webhooks, TwiML Apps, Functions, Studio, or Proxy

A CALL COMES IN:
- Dropdown: Webhook
- URL: https://abc123.ngrok.io/webhooks/incoming-call/
- HTTP: POST

PRIMARY HANDLER FAILS:
- (Leave default or same URL)

CALL STATUS CHANGES:
- URL: https://abc123.ngrok.io/webhooks/call-status/
- HTTP: POST
```

**Important:** Replace `abc123.ngrok.io` with YOUR actual ngrok URL

**E. Click "Save" at the bottom**

---

### Step 5: Test Incoming Call

**Now call your Twilio number from any phone:**
```
Dial: +1 (765) 645-6867
```

**What should happen:**
1. ✅ The call connects (no "invalid number")
2. ✅ Your Django backend receives the webhook
3. ✅ System finds an available agent
4. ✅ If agent1 is available, their client would ring
5. ✅ If no agent available, caller hears "all agents busy" message

**Check the logs:**
```bash
# In your Django terminal, you should see:
tail -f server.log

# You should see something like:
INFO "POST /webhooks/incoming-call/ HTTP/1.1" 200
```

---

## 📱 How Incoming Calls Work

```
Customer Calls
+17656456867
     │
     ▼
┌────────────┐
│   Twilio   │
│   Cloud    │
└─────┬──────┘
      │ Webhook
      │ POST /webhooks/incoming-call/
      ▼
┌──────────────────┐
│  Your Django     │
│  Backend         │
│  (via ngrok)     │
└─────┬────────────┘
      │
      ├─ Finds available agent
      │
      ├─ Returns TwiML to connect
      │
      ▼
┌──────────────────┐
│  Twilio routes   │
│  to agent's      │
│  WebRTC client   │
└──────────────────┘
```

---

## 🧪 Testing Different Scenarios

### Test 1: Call with Available Agent
```bash
# Make sure agent1 is available
curl -X POST http://localhost:8000/api/users/2/set_availability/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"is_available": true}'

# Now call +17656456867
# The call should be routed to agent1's WebRTC client
```

### Test 2: Call with No Available Agent
```bash
# Set all agents to unavailable
curl -X POST http://localhost:8000/api/users/2/set_availability/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"is_available": false}'

# Now call +17656456867
# Caller should hear: "Sorry, all agents are currently busy"
```

### Test 3: Check Call Logs
```bash
# After making a call, check if it was logged
curl http://localhost:8000/api/calls/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# You should see the incoming call in the database
```

---

## 🔍 Debugging Incoming Calls

### Check ngrok Inspector
Open http://127.0.0.1:4040 in your browser to see:
- All webhook requests from Twilio
- Request/response details
- Any errors

### Check Django Logs
```bash
tail -f server.log

# Look for:
INFO "POST /webhooks/incoming-call/ HTTP/1.1" 200
```

### Check Twilio Console
Go to: https://console.twilio.com/us1/monitor/logs/calls

You'll see:
- All incoming calls
- Call duration
- Call status
- Any errors

### Common Issues

**1. Still getting "invalid number"**
- ✅ Check: Is ngrok running?
- ✅ Check: Is Django server running?
- ✅ Check: Did you save Twilio phone number config?
- ✅ Check: Is ALLOWED_HOSTS updated in .env?

**2. Call connects but immediately hangs up**
- ✅ Check: Is the webhook URL correct?
- ✅ Check: Is Django returning valid TwiML?
- ✅ Check: Server logs for errors

**3. "All agents busy" even though agent is available**
- ✅ Check: Is agent's `is_available` set to true?
- ✅ Check: Is agent's `twilio_client_identity` set?

---

## 📲 Next Step: Connect Agent's Phone/Browser

For the agent to actually receive the call, they need a client app:

### Option 1: Web Browser (Quickest Test)

Create a simple HTML file:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Twilio Voice Client</title>
    <script src="https://sdk.twilio.com/js/client/releases/1.14.0/twilio.min.js"></script>
</head>
<body>
    <h1>Agent Voice Client</h1>
    <button id="startup">Connect</button>
    <button id="hangup" disabled>Hang Up</button>
    <div id="log"></div>

    <script>
        let device;
        
        document.getElementById('startup').onclick = async () => {
            // Get token from your API
            const response = await fetch('http://localhost:8000/api/auth/login/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: 'agent1', password: 'test123'})
            });
            const {access} = await response.json();
            
            const tokenResponse = await fetch('http://localhost:8000/api/twilio/token/', {
                method: 'POST',
                headers: {'Authorization': `Bearer ${access}`}
            });
            const {token} = await tokenResponse.json();
            
            // Initialize Twilio Device
            device = new Twilio.Device(token);
            
            device.on('ready', () => {
                document.getElementById('log').innerText = 'Ready to receive calls!';
            });
            
            device.on('incoming', (conn) => {
                document.getElementById('log').innerText = 'Incoming call!';
                conn.accept();
            });
            
            device.on('connect', () => {
                document.getElementById('log').innerText = 'Call connected!';
                document.getElementById('hangup').disabled = false;
            });
        };
        
        document.getElementById('hangup').onclick = () => {
            device.disconnectAll();
        };
    </script>
</body>
</html>
```

Save as `agent_client.html` and open in browser!

### Option 2: Mobile App

Build an Android/iOS app using Twilio Voice SDK that:
1. Gets token from `/api/twilio/token/`
2. Registers for incoming calls
3. Receives calls when routed by backend

---

## ✅ Success Checklist

- [ ] ngrok installed and running
- [ ] Django server restarted with ngrok URL in ALLOWED_HOSTS
- [ ] Twilio phone number configured with ngrok webhook URLs
- [ ] Can call +17656456867 without "invalid number" error
- [ ] Calls are logged in Django admin panel
- [ ] Can see webhook requests in ngrok inspector
- [ ] Agent client ready to receive calls (browser or mobile)

---

## 🎯 Quick Test Commands

```bash
# 1. Start ngrok
ngrok http 8000

# 2. Update .env with ngrok URL
# ALLOWED_HOSTS=localhost,127.0.0.1,YOUR_NGROK_URL

# 3. Restart Django
pkill -f "python manage.py runserver"
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000

# 4. Call your number from any phone
# Dial: +1-765-645-6867

# 5. Check logs
tail -f server.log
```

---

## 🆘 Still Having Issues?

1. Check ngrok inspector: http://127.0.0.1:4040
2. Check Django logs: `tail -f server.log`
3. Check Twilio logs: https://console.twilio.com/us1/monitor/logs/calls
4. Verify phone number config: https://console.twilio.com/us1/develop/phone-numbers/manage/incoming

---

**Your incoming call system is almost ready! Just need to set up ngrok and configure the Twilio number.** 🎉
