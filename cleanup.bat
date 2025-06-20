@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"

echo ========================================
echo   Regular Comix - Cleanup Script
echo ========================================
echo.

echo Deleting duplicate/unused files...
echo.

REM Delete old preview scripts
if exist "preview.py" (
    del "preview.py" >nul 2>&1
    echo [DELETED] preview.py
) else (
    echo [NOT FOUND] preview.py
)

if exist "preview_fixed.py" (
    del "preview_fixed.py" >nul 2>&1
    echo [DELETED] preview_fixed.py
) else (
    echo [NOT FOUND] preview_fixed.py
)

if exist "preview.ps1" (
    del "preview.ps1" >nul 2>&1
    echo [DELETED] preview.ps1
) else (
    echo [NOT FOUND] preview.ps1
)

if exist "preview_results.bat" (
    del "preview_results.bat" >nul 2>&1
    echo [DELETED] preview_results.bat
) else (
    echo [NOT FOUND] preview_results.bat
)

if exist "view_results_fixed.bat" (
    del "view_results_fixed.bat" >nul 2>&1
    echo [DELETED] view_results_fixed.bat
) else (
    echo [NOT FOUND] view_results_fixed.bat
)

echo.
echo ========================================
echo Cleanup completed!
echo ========================================
echo.
echo Remaining useful files:
echo - main.py (main generator)
echo - quick_preview.py (simple preview)
echo - view_results.bat (menu interface)
echo - start_web.bat (web interface)
echo - open_results_folder.bat (open folder)
echo - cleanup.bat (this cleanup script)
echo.
echo You can delete cleanup.bat after use.
echo ========================================

pause
