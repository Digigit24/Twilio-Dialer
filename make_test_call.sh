#!/bin/bash

echo "======================================"
echo "📞 Making a Test Call via API"
echo "======================================"

# Step 1: Login
echo -e "\n1️⃣  Logging in as agent1..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "agent1", "password": "test123"}')

ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['access'])")

if [ -z "$ACCESS_TOKEN" ]; then
    echo "❌ Login failed!"
    exit 1
fi

echo "✅ Login successful!"
echo "Token: ${ACCESS_TOKEN:0:50}..."

# Step 2: Initiate a call
echo -e "\n2️⃣  Initiating call to +1555999TEST..."
CALL_RESPONSE=$(curl -s -X POST http://localhost:8000/api/calls/initiate/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to_number": "+15559991234",
    "from_number": "+17656456867",
    "lead_id": 1,
    "record": true
  }')

echo -e "\n📋 Call Response:"
echo "$CALL_RESPONSE" | python3 -m json.tool

# Check if call was initiated
CALL_SID=$(echo $CALL_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('call_sid', ''))" 2>/dev/null)

if [ ! -z "$CALL_SID" ]; then
    echo -e "\n✅ Call initiated successfully!"
    echo "Call SID: $CALL_SID"
    
    # Step 3: Check call status
    echo -e "\n3️⃣  Checking calls list..."
    sleep 2
    curl -s http://localhost:8000/api/calls/ \
      -H "Authorization: Bearer $ACCESS_TOKEN" | python3 -m json.tool | head -50
else
    echo -e "\n⚠️  Note: Call will be initiated through Twilio"
    echo "This is a REAL call that will be made to the phone number!"
fi

echo -e "\n======================================"
echo "📱 Next Steps:"
echo "======================================"
echo ""
echo "To make REAL calls that actually connect:"
echo ""
echo "1. Set up TwiML App in Twilio Console"
echo "2. Install ngrok: brew install ngrok"
echo "3. Run ngrok: ngrok http 8000"
echo "4. Configure Twilio webhooks with ngrok URL"
echo "5. Update TWILIO_APP_SID in .env"
echo ""
echo "See TESTING_GUIDE.md for detailed instructions!"
echo ""
