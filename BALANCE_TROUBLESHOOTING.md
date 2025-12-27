# 💰 Twilio Balance Troubleshooting Guide

## ⚠️ Getting "Not Enough Balance" Error?

This guide will help you fix balance issues and test your Twilio phone numbers.

---

## 🔍 Quick Diagnosis

### Open This Page in Your Browser:
```
http://localhost:8000/test_config.html
```

This will automatically check:
- ✅ Server connectivity
- ✅ Twilio configuration
- ✅ Authentication
- ⚠️ Balance status

---

## 💡 Understanding Twilio Balance

### Trial Accounts (FREE Testing)
- ✅ Get $15.50 in free trial credits
- ✅ Can call **verified numbers** for FREE
- ⚠️ Calls have "trial account" message
- ❌ Cannot call unverified numbers without credits

### Upgraded Accounts (Paid)
- ✅ Call **any number** worldwide
- ✅ No trial messages
- 💰 Costs: ~$0.013/minute for USA calls
- 💰 Phone rental: ~$1/month

---

## ✅ Solution 1: Verify Your Phone Number (FREE Testing)

**This is the easiest way to test for FREE on trial accounts!**

### Step 1: Go to Twilio Console
```
https://console.twilio.com/us1/develop/phone-numbers/manage/verified
```

### Step 2: Add Your Phone Number
1. Click **"Add a new caller ID"** or **"Verify a number"**
2. Enter your mobile number: `+1234567890` (use E.164 format)
3. Choose verification method: SMS or Call
4. Click **"Verify"**

### Step 3: Get the Verification Code
- Twilio will call or SMS you
- Enter the 6-digit code
- ✅ Your number is now verified!

### Step 4: Test Calling (FREE!)
1. Open: `http://localhost:8000/agent_call_client.html`
2. Login: `agent1` / `test123`
3. Enter your **verified phone number**: `+1234567890`
4. Click "Make Call"
5. **Your phone will ring!** 🎉

**Important:** You can only call verified numbers on trial accounts, but it's completely FREE!

---

## 💳 Solution 2: Add Credits (Call Any Number)

### Step 1: Check Your Current Balance
1. Go to: https://console.twilio.com/
2. Look at the top-right corner
3. You'll see your current balance (e.g., "$0.00")

### Step 2: Add Payment Method
1. Click your account name (top-right)
2. Select **"Billing"** → **"Payment Methods"**
3. Click **"Add Payment Method"**
4. Enter credit card details
5. Click **"Save"**

### Step 3: Add Funds
1. Go to: https://console.twilio.com/billing/add-funds
2. Enter amount: **$20 minimum** (recommended $50 for testing)
3. Click **"Add Funds"**
4. ✅ Credits added instantly!

### Step 4: Test Calling (Any Number!)
1. Open: `http://localhost:8000/agent_call_client.html`
2. Login: `agent1` / `test123`
3. Enter **any phone number**: `+1234567890`
4. Click "Make Call"
5. The call will connect! 🎉

---

## 📱 How to Test Your Phone Number in Browser

### Method 1: Use the Configuration Checker

1. **Start your Django server:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

2. **Open in browser:**
   ```
   http://localhost:8000/test_config.html
   ```

3. **Click "Run Configuration Checks"**
   - ✅ Green = Everything working
   - ❌ Red = Configuration issue
   - ⚠️ Yellow = Balance warning

### Method 2: Use the Agent Call Client

1. **Open in browser:**
   ```
   http://localhost:8000/agent_call_client.html
   ```

2. **Login:**
   - Username: `agent1`
   - Password: `test123`

3. **Check status message:**
   - ✅ "Ready! Connected as user_X" = Configuration is correct
   - ❌ Error = Check your .env file

4. **Try making a call:**
   - Enter a phone number
   - Click "Make Call"
   - **Check the error message** if it fails

---

## 🔧 Common Errors and Solutions

### Error: "21210 - Insufficient funds"
**Cause:** No money in Twilio account

**Solution:**
- **Option A (FREE):** Verify your phone number (see Solution 1 above)
- **Option B (PAID):** Add credits (see Solution 2 above)

### Error: "21212 - Cannot call unverified number"
**Cause:** Trial account trying to call unverified number

**Solution:**
1. Verify the destination number:
   - Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/verified
   - Add and verify the number
2. OR upgrade your account and add credits

### Error: "Authentication Failed"
**Cause:** Wrong Twilio credentials in .env

**Solution:**
1. Check your .env file:
   ```env
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx    # From console.twilio.com
   TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxx    # From console.twilio.com
   ```
2. Get correct values from: https://console.twilio.com/
3. Restart the server after updating .env

### Error: "Invalid phone number"
**Cause:** Wrong phone number format

**Solution:**
- Use E.164 format: `+1234567890`
- Include country code: `+1` for USA
- No spaces, dashes, or parentheses

---

## 📊 Understanding Twilio Costs

### What You'll Pay (After Trial Credits):

**Phone Number Rental:**
- Local number (USA): $1.00/month
- Toll-free number: $2.00/month

**Outbound Calls:**
- USA: $0.013/minute
- Canada: $0.013/minute
- UK: $0.021/minute
- Other countries: varies

**Incoming Calls:**
- Local number (USA): $0.0085/minute

**Example Cost Calculation:**
- 100 minutes of calls: ~$1.30
- 1 phone number: $1.00/month
- **Total for 100 minutes:** ~$2.30

---

## 🎯 Recommended Testing Path

### For Development/Testing:

1. **Use trial account with verified numbers (FREE):**
   ```
   ✅ Verify 2-3 test phone numbers
   ✅ Make unlimited FREE calls to verified numbers
   ✅ Test all features without spending money
   ⚠️ Accept the "trial account" message
   ```

2. **When ready for production:**
   ```
   💳 Upgrade account
   💰 Add $50 in credits
   📞 Call any number worldwide
   🔊 No trial messages
   ```

---

## 📋 Quick Testing Checklist

**Before Testing:**
- [ ] Django server is running: `python manage.py runserver 0.0.0.0:8000`
- [ ] .env file has correct Twilio credentials
- [ ] Test users are created: `python create_test_users.py`

**For FREE Testing (Trial):**
- [ ] Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/verified
- [ ] Verify your mobile number
- [ ] Get the verification code
- [ ] Number shows as "Verified" in console
- [ ] Open: http://localhost:8000/agent_call_client.html
- [ ] Login: agent1 / test123
- [ ] Call your verified number
- [ ] Call connects (with trial message)

**For Paid Testing:**
- [ ] Check balance: https://console.twilio.com/
- [ ] Add payment method
- [ ] Add funds ($20 minimum)
- [ ] Balance shows in console
- [ ] Open: http://localhost:8000/agent_call_client.html
- [ ] Login: agent1 / test123
- [ ] Call any phone number
- [ ] Call connects (no trial message)

---

## 🔗 Important Links

| Purpose | URL |
|---------|-----|
| **Check Balance** | https://console.twilio.com/ |
| **Verify Phone Numbers (FREE)** | https://console.twilio.com/us1/develop/phone-numbers/manage/verified |
| **Add Funds** | https://console.twilio.com/billing/add-funds |
| **Call Logs** | https://console.twilio.com/monitor/logs/calls |
| **Phone Numbers** | https://console.twilio.com/us1/develop/phone-numbers/manage/active |
| **TwiML Apps** | https://console.twilio.com/us1/develop/voice/manage/twiml-apps |

---

## 🧪 Test Configuration (Browser)

### Option 1: Automatic Checker
```
http://localhost:8000/test_config.html
```
- Runs automatic diagnostics
- Shows exact errors
- Provides solutions

### Option 2: Manual Testing
```
http://localhost:8000/agent_call_client.html
```
- Login and test calling
- See real-time errors
- Make actual calls

---

## 💡 Pro Tips

1. **Start with verified numbers:**
   - Verify your mobile, office phone, and a friend's phone
   - Test completely FREE on trial account

2. **Monitor your usage:**
   - Check: https://console.twilio.com/billing/usage
   - Set up usage alerts

3. **Check call logs for errors:**
   - https://console.twilio.com/monitor/logs/calls
   - Shows detailed error messages and reasons

4. **Use browser console (F12):**
   - See detailed JavaScript errors
   - Check network requests
   - Identify issues quickly

5. **Keep credits topped up:**
   - Add funds when balance < $10
   - Prevents failed calls in production

---

## 🎯 Summary

**No Balance? Two Options:**

### FREE Testing (Recommended for Development)
```
1. Go to Twilio Console → Verified Caller IDs
2. Verify your phone number
3. Call it for FREE from the app
4. Unlimited testing at no cost!
```

### Paid Calling (For Production)
```
1. Go to Twilio Console → Billing
2. Add payment method
3. Add $20-50 in credits
4. Call any number worldwide
```

---

**Questions? Check the call logs:** https://console.twilio.com/monitor/logs/calls

**Need help? Open the test page:** http://localhost:8000/test_config.html
