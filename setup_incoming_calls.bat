@echo off
echo ================================================================
echo       Setting Up Incoming Calls for Windows - Step by Step
echo ================================================================
echo.

REM Step 1: Check if ngrok is installed
echo Step 1: Checking for ngrok...
where ngrok >nul 2>nul
if %errorlevel% == 0 (
    echo [OK] ngrok is already installed!
    ngrok version
) else (
    echo [!] ngrok is not installed
    echo.
    echo Please download ngrok for Windows:
    echo 1. Go to: https://ngrok.com/download
    echo 2. Download the Windows ZIP file
    echo 3. Extract ngrok.exe to C:\Windows\System32 or add to PATH
    echo 4. Run this script again
    echo.
    pause
    exit /b
)

echo.
echo ================================================================
echo.

REM Step 2: ngrok authentication
echo Step 2: ngrok Authentication
echo.
echo To use ngrok, you need a free account:
echo 1. Go to: https://dashboard.ngrok.com/signup
echo 2. Sign up (it's free!)
echo 3. Get your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken
echo.
set /p authtoken="Enter your ngrok auth token (or press Enter to skip): "

if not "%authtoken%"=="" (
    ngrok config add-authtoken %authtoken%
    echo [OK] Auth token configured!
) else (
    echo [!] Skipped auth token configuration
    echo     You'll need to do this manually: ngrok config add-authtoken YOUR_TOKEN
)

echo.
echo ================================================================
echo.

REM Step 3: Instructions
echo Step 3: Start ngrok
echo.
echo Open a NEW Command Prompt window and run:
echo.
echo     ngrok http 8000
echo.
echo After starting ngrok, you'll get a URL like:
echo     https://abc123.ngrok.io
echo.
echo ================================================================
echo.

REM Step 4: Next steps
echo NEXT STEPS:
echo.
echo 1. Open a new Command Prompt and run:
echo    ngrok http 8000
echo.
echo 2. Copy the https:// URL (e.g., https://abc123.ngrok.io)
echo.
echo 3. Edit .env file and update ALLOWED_HOSTS:
echo    ALLOWED_HOSTS=localhost,127.0.0.1,abc123.ngrok.io
echo    (Replace abc123.ngrok.io with YOUR ngrok URL, without https://)
echo.
echo 4. Restart Django server:
echo    - Press Ctrl+C to stop current server
echo    - Run: venv\Scripts\activate
echo    - Run: python manage.py runserver 0.0.0.0:8000
echo.
echo 5. Configure Twilio phone number:
echo    Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/incoming
echo    Click on: +17656456867
echo    Set 'A CALL COMES IN' to: https://YOUR_NGROK_URL/webhooks/incoming-call/
echo    Set 'CALL STATUS CHANGES' to: https://YOUR_NGROK_URL/webhooks/call-status/
echo    Click 'Save'
echo.
echo 6. Test by calling: +1 (765) 645-6867
echo.
echo ================================================================
echo.
echo [OK] Setup script complete!
echo.
echo See INCOMING_CALLS_SETUP.md for detailed instructions.
echo.
pause
