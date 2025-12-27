@echo off
echo ========================================
echo    Fixing All Git Merge Conflicts
echo ========================================
echo.

echo [1/2] Fixing twilio_crm\urls.py...
copy /Y twilio_crm_urls_CLEAN.py twilio_crm\urls.py >nul
if %errorlevel% equ 0 (
    echo     ✓ Fixed twilio_crm\urls.py
) else (
    echo     ✗ Failed to fix twilio_crm\urls.py
)

echo.
echo [2/2] Fixing calls\services.py...
copy /Y calls_services_CLEAN.py calls\services.py >nul
if %errorlevel% equ 0 (
    echo     ✓ Fixed calls\services.py
) else (
    echo     ✗ Failed to fix calls\services.py
)

echo.
echo ========================================
echo    All merge conflicts fixed!
echo ========================================
echo.
echo Now you can run:
echo     python manage.py runserver 0.0.0.0:8000
echo.
echo Then open: http://localhost:8000/
echo.
pause
