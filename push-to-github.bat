@echo off
echo ===================================================
echo   Django Girls Freetown - Push Updates to GitHub
echo ===================================================
echo.
cd /d "%~dp0"

echo Checking Git status...
git status
echo.

echo Adding all modified and new files...
git add -A

echo Committing changes...
git commit -m "Update profile avatar display, add Django Girls favicon, and clean portfolio docs footers"

echo Pushing to GitHub (origin main)...
git push origin main

echo.
if %errorlevel% neq 0 (
    echo [ERROR] Git push failed. Please verify your GitHub access or credentials.
) else (
    echo [SUCCESS] Successfully pushed all updates to GitHub!
)
echo.
pause
