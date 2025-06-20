@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"

echo.
echo ==========================================
echo   Regular Comix - Launcher
echo ==========================================

REM 尋找 PowerShell（多種方式）
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

REM 方法1：如果找到 PowerShell，提供選項
if defined PS_FOUND (
    if exist "launcher.ps1" (
        echo [Option 1] PowerShell Launcher (Best Chinese support)
        echo [Option 2] Windows Optimized Python Launcher  
        echo [Option 3] Simple Batch Menu
        echo.
        set /p choice="Choose (1/2/3): "
        
        if "!choice!"=="1" (
            echo Starting PowerShell launcher...
            "%PS_FOUND%" -ExecutionPolicy Bypass -File "launcher.ps1"
            exit /b
        )
        
        if "!choice!"=="2" (
            echo Starting Windows optimized launcher...
            python launcher_windows.py
            exit /b
        )
    )
)

REM 方法2：簡化版批次檔選單
echo Using simple batch menu...
echo.
echo Available options:
echo  1. Generate new content
echo  2. Start web interface  
echo  3. Open results folder
echo  4. Exit
echo.

:menu
set /p choice="Select (1-4): "

if "%choice%"=="1" (
    echo.
    echo Generating content...
    set PYTHONIOENCODING=utf-8
    python main.py
    echo.
    pause
    goto menu
)

if "%choice%"=="2" (
    echo.
    echo Starting web interface...
    
    REM 優先嘗試 PowerShell
    if defined PS_FOUND (
        if exist "start_web.ps1" (
            "%PS_FOUND%" -ExecutionPolicy Bypass -File "start_web.ps1" 2>nul
            if not errorlevel 1 goto menu
        )
    )
    
    REM 備用方案：直接啟動
    echo Using direct launcher...
    call start_web_direct.bat
    goto menu
)

if "%choice%"=="3" (
    echo.
    echo Opening results folder...
    if exist "docs\outputs" (
        explorer "docs\outputs"
        echo Results folder opened.
    ) else (
        echo Results folder not found.
    )
    echo.
    pause
    goto menu
)

if "%choice%"=="4" (
    echo Goodbye!
    exit /b
)

echo Invalid choice. Please try again.
goto menu
