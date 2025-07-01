@echo off
REM Regular Comix Launcher
REM 簡潔版啟動器，避免編碼問題

cd /d "%~dp0"

REM 設定編碼為 UTF-8
chcp 65001 >nul

echo.
echo ==========================================
echo   Regular Comix Launcher
echo ==========================================
echo.

REM 檢查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python and add it to PATH.
    pause
    exit /b 1
)

REM 檢查啟動文件
if not exist "launcher.py" (
    echo ERROR: launcher.py not found!
    pause
    exit /b 1
)

echo Starting Regular Comix...
echo Please wait while the program loads...
echo.

REM 設定 Python 環境變數
set PYTHONIOENCODING=utf-8
set PYTHONLEGACYWINDOWSSTDIO=utf-8
set PYTHONUNBUFFERED=1

REM 使用 cmd 來執行 Python，確保更好的交互性
cmd /c "python launcher.py"

echo.
echo Program finished.
pause
