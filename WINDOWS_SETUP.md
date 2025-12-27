# 📞 Windows Setup Guide - Enable Incoming Calls

## Quick Setup for Windows Users

Follow these steps to fix the "invalid number" issue on Windows.

---

## Step 1: Download ngrok

1. Go to: https://ngrok.com/download
2. Click **"Download For Windows"**
3. Extract the ZIP file
4. Move `ngrok.exe` to: `C:\ngrok\ngrok.exe`
5. Add to PATH:
   - Press `Win + X` → **System**
   - Click **Advanced system settings**
   - Click **Environment Variables**
   - Under **System variables**, find **Path**, click **Edit**
   - Click **New** and add: `C:\ngrok`
   - Click **OK** on all windows

**Verify installation:**
```cmd
ngrok version
```

---

## Step 2: Sign Up for ngrok (FREE)

1. Go to: https://dashboard.ngrok.com/signup
2. Sign up with email (completely free)
3. After signing up, go to: https://dashboard.ngrok.com/get-started/your-authtoken
4. Copy your authtoken

**Configure ngrok:**
```cmd
ngrok config add-authtoken YOUR_COPIED_TOKEN
```

---

## Step 3: Start ngrok

**Open Command Prompt** (Win + R, type `cmd`, Enter)

```cmd
cd C:\path\to\Twilio-Dialer
ngrok http 8000
```

**You'll see something like this:**
```
ngrok                                                           

Session Status                online
Region                        United States (us)
Forwarding                    https://abc123.ngrok.io -> http://localhost:8000
                              ^^^^^^^^^^^^^^^^^^^^
                              THIS IS YOUR PUBLIC URL!
```

**IMPORTANT:** Keep this window open! Copy the URL: `https://abc123.ngrok.io`

---

## Step 4: Update .env File

1. Open `.env` file in Notepad:
   ```cmd
   notepad .env
   ```

2. Find this line:
   ```
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

3. Change it to (use YOUR ngrok URL):
   ```
   ALLOWED_HOSTS=localhost,127.0.0.1,abc123.ngrok.io
   ```
   
   **Note:** Don't include `https://` - just the domain!

4. Save and close Notepad

---

## Step 5: Restart Django Server

**In your Django terminal:**

1. Press `Ctrl + C` to stop the server
2. Activate virtual environment:
   ```cmd
   venv\Scripts\activate
   ```
3. Start server again:
   ```cmd
   python manage.py runserver 0.0.0.0:8000
   ```

---

## Step 6: Configure Twilio Phone Number

1. Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/incoming

2. Click on your number: **+17656456867**

3. Scroll down to **"Voice Configuration"**

4. Fill in these fields:

   **Configure with:** 
   - Select: `Webhooks, TwiML Apps, Functions, Studio, or Proxy`

   **A CALL COMES IN:**
   - Dropdown: `Webhook`
   - URL: `https://abc123.ngrok.io/webhooks/incoming-call/`
   - HTTP: `POST`

   **CALL STATUS CHANGES:**
   - URL: `https://abc123.ngrok.io/webhooks/call-status/`
   - HTTP: `POST`

   **Replace `abc123.ngrok.io` with YOUR actual ngrok URL!**

5. Scroll down and click **"Save"**

---

## Step 7: Test It!

**Call your Twilio number from any phone:**
```
📞 Dial: +1-765-645-6867
```

**What should happen:**
✅ Call connects (NO "invalid number"!)
✅ You hear: "Sorry, all agents are currently busy"
✅ Call is logged in your Django admin

**Check if it worked:**
1. Go to: http://localhost:8000/admin
2. Login with: `admin` / `admin123`
3. Click **Calls** - you should see the incoming call!

---

## 🔍 Debugging

**Still getting "invalid number"?**

### Check 1: Is ngrok running?
- Look for the ngrok window
- Should show "Session Status: online"

### Check 2: Is Django running?
- Look for the Django server window
- Should show "Starting development server at..."

### Check 3: Did you save Twilio config?
- Go back to Twilio Console
- Check that webhook URLs are saved
- Make sure URLs start with `https://` (not `http://`)

### Check 4: Check .env file
```cmd
notepad .env
```
Make sure ALLOWED_HOSTS has your ngrok domain

### Check 5: View ngrok inspector
Open browser: http://127.0.0.1:4040

You should see webhook requests from Twilio when someone calls.

---

## 📋 Quick Reference

**Terminal 1 - ngrok:**
```cmd
ngrok http 8000
```

**Terminal 2 - Django:**
```cmd
cd C:\path\to\Twilio-Dialer
venv\Scripts\activate
python manage.py runserver 0.0.0.0:8000
```

**Twilio Phone Config:**
- Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/incoming
- Number: +17656456867
- Webhook: `https://YOUR_NGROK_URL/webhooks/incoming-call/`

**Test:**
- Call: +1-765-645-6867
- Should NOT say "invalid number"

---

## 🎯 Common Windows Issues

### Issue 1: "ngrok is not recognized"
**Solution:** Add ngrok to PATH (see Step 1)

### Issue 2: "Port 8000 is already in use"
**Solution:** 
```cmd
# Find and kill the process
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

### Issue 3: Virtual environment activation fails
**Solution:**
```cmd
# Use PowerShell instead
.\venv\Scripts\Activate.ps1

# Or use full path
C:\path\to\Twilio-Dialer\venv\Scripts\activate
```

### Issue 4: Can't edit .env file
**Solution:**
```cmd
# Open with different editor
notepad .env

# Or use VS Code
code .env
```

---

## ✅ Success Checklist

- [ ] ngrok installed and in PATH
- [ ] ngrok auth token configured
- [ ] ngrok running with public URL
- [ ] .env updated with ngrok domain
- [ ] Django server restarted
- [ ] Twilio phone number configured with webhooks
- [ ] Can call +17656456867 without "invalid number"
- [ ] Call appears in Django admin panel

---

## 🚀 You're Done!

After completing these steps:
✅ Customers can call +17656456867
✅ Calls connect (no "invalid number")
✅ Calls are logged in your CRM
✅ System routes to available agents

---

## 📞 Support

- Detailed guide: `INCOMING_CALLS_SETUP.md`
- API docs: http://localhost:8000/api/docs/
- Admin panel: http://localhost:8000/admin

**Need more help?** Check the ngrok inspector at http://127.0.0.1:4040
