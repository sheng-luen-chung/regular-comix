@echo off
REM Simple Web Launcher - 直接啟動網頁界面（避免 PowerShell 問題）
chcp 65001 >nul 2>&1
cd /d "%~dp0"

echo.
echo ==========================================
echo   Regular Comix - Web Interface
echo ==========================================
echo   Simple web launcher (No PowerShell needed)
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found
    echo Please install Python or add it to PATH
    pause
    exit /b 1
)

REM Check web directory
if not exist "web\app.py" (
    echo Error: web\app.py not found
    echo Please make sure you are in the correct directory
    pause
    exit /b 1
)

echo Starting web server...
echo.
echo Browser URL: http://127.0.0.1:5000
echo.
echo Features:
echo  - Browse comic scripts
echo  - Play audio files  
echo  - Download content
echo.
echo Press Ctrl+C to stop server
echo ==========================================
echo.

REM Set encoding
set PYTHONIOENCODING=utf-8
set PYTHONLEGACYWINDOWSSTDIO=utf-8

REM Start Flask
cd web
python app.py

echo.
echo Server stopped.
pause
