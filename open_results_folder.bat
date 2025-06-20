@echo off
chcp 65001 >nul 2>&1

echo.
echo ========================================
echo   Regular Comix - Open Results Folder
echo ========================================
echo.

set "results_folder=%~dp0docs\outputs"

if exist "%results_folder%" (
    echo Opening results folder...
    echo Location: %results_folder%
    echo.
    start "" "%results_folder%"
    echo.
    echo Folder opened in File Explorer.
    echo You can:
    echo - Double-click .txt files to read scripts
    echo - Double-click .mp3 files to play audio
    echo.
) else (
    echo No results folder found.
    echo Please run: python main.py
    echo.
)

pause
