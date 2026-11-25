@echo off
cd /d "%~dp0"
if not exist "C:\xampp\php\php.exe" (
 echo XAMPP PHP not found. Edit this file if XAMPP is installed elsewhere.
 pause
 exit /b 1
)
if not exist config.local.php copy config.example.php config.local.php >nul
echo Start MySQL in XAMPP and create database django_girls in phpMyAdmin first.
echo Update config.local.php if your database credentials are different.
pause
"C:\xampp\php\php.exe" tools\install.php
pause
