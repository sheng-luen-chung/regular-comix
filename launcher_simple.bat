@echo off
REM Regular Comix - 簡化啟動器（避免中文亂碼）
chcp 65001 >nul 2>&1
cd /d "%~dp0"

echo.
echo ==========================================
echo   Regular Comix - Comic Script Generator
echo ==========================================
echo.

REM Check for PowerShell (recommended)
where powershell.exe >nul 2>&1
if not errorlevel 1 (
    if exist "launcher.ps1" (
        echo [1] Use PowerShell launcher (Best Chinese support)
        echo [2] Use Batch launcher (Basic)
        echo.
        set /p choice="Choose (1/2): "
        if "!choice!"=="1" (
            echo Starting PowerShell launcher...
            powershell.exe -ExecutionPolicy Bypass -File "launcher.ps1"
            exit /b
        )
    )
)

echo Using basic launcher...
echo.
echo Features:
echo  1. Generate new comic scripts
echo  2. Start web interface
echo  3. Open results folder
echo  4. Quick preview
echo  5. Clean old files
echo  6. Exit
echo.

:menu
echo ==========================================
set /p choice="Select option (1-6): "

if "%choice%"=="1" (
    echo.
    echo Generating new content...
    python main.py
    echo.
    echo Press any key to continue...
    pause >nul
    goto menu
)

if "%choice%"=="2" (
    echo.
    echo Starting web interface...
    if exist "start_web.ps1" (
        powershell.exe -ExecutionPolicy Bypass -File "start_web.ps1"
    ) else (
        call start_web.bat
    )
    goto menu
)

if "%choice%"=="3" (
    echo.
    echo Opening results folder...
    if exist "docs\outputs" (
        explorer "docs\outputs"
    ) else (
        echo Error: Results folder not found
    )
    echo.
    echo Press any key to continue...
    pause >nul
    goto menu
)

if "%choice%"=="4" (
    echo.
    echo Quick preview...
    python -c "
import os
from pathlib import Path
outputs_dir = Path('docs/outputs')
if outputs_dir.exists():
    batches = sorted([d.name for d in outputs_dir.iterdir() if d.is_dir()], reverse=True)
    if batches:
        latest = batches[0]
        latest_dir = outputs_dir / latest
        files = list(latest_dir.glob('*.txt'))
        print(f'Latest batch: {latest}')
        print(f'Scripts found: {len(files)}')
        for i, f in enumerate(files[:3], 1):
            print(f'{i}. {f.stem}')
    else:
        print('No results found')
else:
    print('Results folder not found')
"
    echo.
    echo Press any key to continue...
    pause >nul
    goto menu
)

if "%choice%"=="5" (
    echo.
    echo Cleaning old files...
    python -c "
import os, shutil
from datetime import datetime, timedelta
from pathlib import Path
outputs_dir = Path('docs/outputs')
if outputs_dir.exists():
    cutoff = datetime.now() - timedelta(days=30)
    deleted = 0
    for batch_dir in outputs_dir.iterdir():
        if batch_dir.is_dir():
            try:
                date_str = batch_dir.name[:8]
                batch_date = datetime.strptime(date_str, '%Y%m%d')
                if batch_date < cutoff:
                    shutil.rmtree(batch_dir)
                    deleted += 1
            except:
                pass
    print(f'Cleaned {deleted} old batches')
else:
    print('Results folder not found')
"
    echo.
    echo Press any key to continue...
    pause >nul
    goto menu
)

if "%choice%"=="6" (
    echo.
    echo Goodbye!
    exit /b
)

echo Invalid choice. Please select 1-6.
goto menu
