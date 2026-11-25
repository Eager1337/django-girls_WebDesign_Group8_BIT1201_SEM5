@echo off
echo ===================================================
echo   Copy Django Girls Favicon to XAMPP Root
echo ===================================================
echo.
cd /d "%~dp0"
if exist "C:\xampp\htdocs" (
    copy /Y "favicon.ico" "C:\xampp\htdocs\favicon.ico"
    echo [SUCCESS] Copied favicon.ico to C:\xampp\htdocs\favicon.ico!
    echo Refresh http://localhost/ in your browser (Ctrl + F5).
) else (
    echo C:\xampp\htdocs was not found in the default location.
    echo Please copy favicon.ico to your XAMPP htdocs folder manually.
)
echo.
pause
