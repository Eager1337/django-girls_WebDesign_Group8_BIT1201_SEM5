@echo off
setlocal
cd /d "%~dp0"
echo This additive upgrade retains your database, config.local.php and uploads.
echo Back up your database in phpMyAdmin and copy your project folder first.
if not exist config.local.php (
 echo Missing config.local.php. Keep the configuration from your existing installation.
 pause
 exit /b 1
)
if not exist C:\xampp\php\php.exe (
 echo PHP not found at C:\xampp\php\php.exe. Run tools\upgrade.php with your PHP CLI.
 pause
 exit /b 1
)
"C:\xampp\php\php.exe" tools\upgrade.php
if errorlevel 1 (
 echo Upgrade failed. Read the error above. Do not run the fresh installer.
 pause
 exit /b 1
)
echo Upgrade complete. Open your existing localhost project.
pause