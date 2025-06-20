@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"

REM 嘗試多種方式找到 PowerShell
set "PS_FOUND="
where powershell.exe >nul 2>&1 && set "PS_FOUND=powershell.exe"
if not defined PS_FOUND (
    where pwsh.exe >nul 2>&1 && set "PS_FOUND=pwsh.exe"
)
if not defined PS_FOUND (
    if exist "%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" (
        set "PS_FOUND=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
    )
)

if defined PS_FOUND (
    if exist "start_web.ps1" (
        echo 🚀 使用 PowerShell 啟動網頁界面...
        "%PS_FOUND%" -ExecutionPolicy Bypass -File "start_web.ps1"
        exit /b
    )
)

echo.
echo ========================================
echo   Regular Comix - 網頁界面啟動器
echo ========================================
echo   🎭 四格漫畫腳本與語音產生系統
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 錯誤：系統中找不到 Python
    echo    請安裝 Python 或將其加入 PATH 環境變數
    echo.
    pause
    exit /b 1
)

REM Check if web directory exists
if not exist "web" (
    echo ❌ 錯誤：找不到 web 目錄
    echo    請確認您在正確的專案目錄中
    echo.
    pause
    exit /b 1
)

echo 🚀 正在啟動網頁伺服器...
echo.
echo 📱 請在瀏覽器中開啟以下網址：
echo    ➡️  http://127.0.0.1:5000
echo.
echo 💡 功能說明：
echo    • 瀏覽所有生成的四格漫畫腳本
echo    • 收聽 AI 生成的語音檔案
echo    • 按時間批次查看結果
echo.
echo ⛔ 按 Ctrl+C 可停止伺服器
echo ========================================
echo.

cd web
set PYTHONIOENCODING=utf-8
set PYTHONLEGACYWINDOWSSTDIO=utf-8

REM Start Flask app
python app.py

echo.
echo 🛑 伺服器已停止
echo.
pause
