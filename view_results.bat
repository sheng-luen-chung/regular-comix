@echo off
chcp 65001 >nul 2>&1

echo.
echo ========================================
echo   Regular Comix - View Results
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found in PATH
    echo Please install Python or add it to PATH
    pause
    exit /b 1
)

echo Choose an option:
echo 1. Quick Preview (command line)
echo 2. Web Interface (browser)
echo.
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Running quick preview...
    python quick_preview.py
) else if "%choice%"=="2" (
    echo.
    echo Starting web interface...
    echo Please open: http://127.0.0.1:5000
    echo.
    cd /d "%~dp0\web"
    set PYTHONIOENCODING=utf-8
    python app.py
) else (
    echo Invalid choice. Running quick preview...
    python quick_preview.py
)

pause
