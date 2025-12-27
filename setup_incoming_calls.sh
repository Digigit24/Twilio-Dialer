#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║      📞 Setting Up Incoming Calls - Step by Step              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Check if ngrok is installed
echo "Step 1: Checking for ngrok..."
if command -v ngrok &> /dev/null; then
    echo "✅ ngrok is already installed!"
    ngrok version
else
    echo "❌ ngrok is not installed"
    echo ""
    echo "📥 Installing ngrok..."
    echo ""
    echo "Please choose your system:"
    echo "1) macOS (using Homebrew)"
    echo "2) Linux"
    echo "3) I'll install it manually"
    echo ""
    read -p "Enter choice (1-3): " choice
    
    case $choice in
        1)
            echo "Installing via Homebrew..."
            brew install ngrok
            ;;
        2)
            echo "Downloading ngrok for Linux..."
            wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
            tar xvzf ngrok-v3-stable-linux-amd64.tgz
            sudo mv ngrok /usr/local/bin/
            rm ngrok-v3-stable-linux-amd64.tgz
            echo "✅ ngrok installed!"
            ;;
        3)
            echo ""
            echo "Please download ngrok from: https://ngrok.com/download"
            echo "Then run this script again."
            exit 0
            ;;
    esac
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

# Step 2: ngrok authentication
echo "Step 2: ngrok Authentication"
echo ""
echo "To use ngrok, you need a free account:"
echo "1. Go to: https://dashboard.ngrok.com/signup"
echo "2. Sign up (it's free!)"
echo "3. Get your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken"
echo ""
read -p "Enter your ngrok auth token (or press Enter to skip): " authtoken

if [ ! -z "$authtoken" ]; then
    ngrok config add-authtoken $authtoken
    echo "✅ Auth token configured!"
else
    echo "⚠️  Skipped auth token configuration"
    echo "   You'll need to do this manually: ngrok config add-authtoken YOUR_TOKEN"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

# Step 3: Instructions
echo "Step 3: Start ngrok"
echo ""
echo "Run this command in a NEW terminal window:"
echo ""
echo "    ngrok http 8000"
echo ""
echo "After starting ngrok, you'll get a URL like:"
echo "    https://abc123.ngrok.io"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

# Step 4: Next steps
echo "📋 NEXT STEPS:"
echo ""
echo "1. Start ngrok in a new terminal:"
echo "   ngrok http 8000"
echo ""
echo "2. Copy the https:// URL (e.g., https://abc123.ngrok.io)"
echo ""
echo "3. Update .env file:"
echo "   ALLOWED_HOSTS=localhost,127.0.0.1,abc123.ngrok.io"
echo "   (Replace abc123.ngrok.io with YOUR ngrok URL, without https://)"
echo ""
echo "4. Restart Django server:"
echo "   pkill -f 'python manage.py runserver'"
echo "   source venv/bin/activate"
echo "   python manage.py runserver 0.0.0.0:8000"
echo ""
echo "5. Configure Twilio phone number:"
echo "   Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/incoming"
echo "   Click on: +17656456867"
echo "   Set 'A CALL COMES IN' to: https://YOUR_NGROK_URL/webhooks/incoming-call/"
echo "   Set 'CALL STATUS CHANGES' to: https://YOUR_NGROK_URL/webhooks/call-status/"
echo "   Click 'Save'"
echo ""
echo "6. Test by calling: +1 (765) 645-6867"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "✅ Setup script complete!"
echo ""
echo "See INCOMING_CALLS_SETUP.md for detailed instructions."
echo ""
