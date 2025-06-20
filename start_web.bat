@echo off
chcp 65001 >nul 2>&1
echo.
echo ========================================
echo   Regular Comix - View Results
echo ========================================
echo.
echo Starting Web Interface...
echo Please open: http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop server
echo ========================================
echo.
cd /d "%~dp0\web"
set PYTHONIOENCODING=utf-8
set PYTHONLEGACYWINDOWSSTDIO=utf-8
python app.py
pause
