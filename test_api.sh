#!/bin/bash

echo "======================================"
echo "🧪 Testing Twilio CRM API"
echo "======================================"

# 1. Login
echo -e "\n1️⃣  Testing Login..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "agent1", "password": "test123"}')

ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['access'])")

if [ -z "$ACCESS_TOKEN" ]; then
    echo "❌ Login failed!"
    exit 1
fi

echo "✅ Login successful! Token received."

# 2. Get User Profile
echo -e "\n2️⃣  Testing Get User Profile..."
curl -s http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" | python3 -m json.tool

# 3. Generate Twilio Token
echo -e "\n3️⃣  Testing Twilio Token Generation..."
curl -s -X POST http://localhost:8000/api/twilio/token/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" | python3 -m json.tool

# 4. Create a Lead
echo -e "\n4️⃣  Testing Create Lead..."
curl -s -X POST http://localhost:8000/api/leads/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "Lead",
    "phone_number": "+1555123456",
    "email": "test@example.com",
    "company": "Test Corp",
    "status": "NEW"
  }' | python3 -m json.tool

# 5. Get Leads
echo -e "\n5️⃣  Testing Get Leads..."
curl -s http://localhost:8000/api/leads/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" | python3 -m json.tool

# 6. Get Call Statistics
echo -e "\n6️⃣  Testing Get Call Statistics..."
curl -s http://localhost:8000/api/statistics/calls/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" | python3 -m json.tool

echo -e "\n======================================"
echo "✅ All API tests completed!"
echo "======================================"
