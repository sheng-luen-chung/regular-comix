# Regular Comix Launcher
# 整合啟動器

# 設定 UTF-8 編碼
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

# 設定環境變數
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONLEGACYWINDOWSSTDIO = "utf-8"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Regular Comix - 整合啟動器" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {
    python launcher.py
} catch {
    Write-Host "❌ 啟動失敗：$_" -ForegroundColor Red
    Read-Host "按 Enter 結束"
}
