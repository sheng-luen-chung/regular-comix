@echo off
chcp 65001 >nul
title Regular Comix - 同步到 GitHub Pages

echo 🚀 Regular Comix 內容同步工具
echo ====================================
echo.

echo 📁 正在掃描 docs/outputs/ 目錄...
python update_file_list.py

echo.
echo 💡 提示：此工具會自動掃描 docs/outputs/ 下的所有批次
echo    並詢問是否要推送到 GitHub Pages
echo.
pause
