@echo off
echo ========================================
echo    Fixing ALL Git Merge Conflicts
echo ========================================
echo.

echo [1/3] Fixing twilio_crm\urls.py...
copy /Y twilio_crm_urls_CLEAN.py twilio_crm\urls.py >nul
if %errorlevel% equ 0 (
    echo     ✓ Fixed twilio_crm\urls.py
) else (
    echo     ✗ Failed to fix twilio_crm\urls.py
)

echo.
echo [2/3] Fixing calls\services.py...
copy /Y calls_services_CLEAN.py calls\services.py >nul
if %errorlevel% equ 0 (
    echo     ✓ Fixed calls\services.py
) else (
    echo     ✗ Failed to fix calls\services.py
)

echo.
echo [3/3] Fixing templates\agent_call_client.html...
if not exist templates mkdir templates
copy /Y agent_call_client_CLEAN.html templates\agent_call_client.html >nul
if %errorlevel% equ 0 (
    echo     ✓ Fixed templates\agent_call_client.html
) else (
    echo     ✗ Failed to fix templates\agent_call_client.html
)

echo.
echo ========================================
echo    All merge conflicts FIXED!
echo ========================================
echo.
echo Now restart your server:
echo.
echo   1. Press CTRL+C to stop current server
echo   2. Run: python manage.py runserver 0.0.0.0:8000
echo   3. Refresh browser: http://localhost:8000/
echo.
pause
