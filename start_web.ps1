# Regular Comix Web Interface Launcher
# 網頁界面啟動器

# 設定 UTF-8 編碼
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Regular Comix - 網頁界面啟動器" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   🎭 四格漫畫腳本與語音產生系統" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 檢查 Python
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "✅ Python 已安裝：$pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 錯誤：系統中找不到 Python" -ForegroundColor Red
    Write-Host "   請安裝 Python 或將其加入 PATH 環境變數" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "按 Enter 結束"
    exit 1
}

# 檢查 web 目錄
if (-not (Test-Path "web\app.py")) {
    Write-Host "❌ 錯誤：找不到 web\app.py" -ForegroundColor Red
    Write-Host "   請確認您在正確的專案目錄中" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "按 Enter 結束"
    exit 1
}

# 檢查輸出目錄
$outputsDir = "docs\outputs"
if (Test-Path $outputsDir) {
    $batches = Get-ChildItem $outputsDir -Directory
    Write-Host "📊 發現 $($batches.Count) 個批次" -ForegroundColor Green
    if ($batches.Count -gt 0) {
        $latest = ($batches | Sort-Object Name -Descending)[0].Name
        Write-Host "📅 最新批次：$latest" -ForegroundColor Cyan
    }
} else {
    Write-Host "⚠️  警告：找不到輸出目錄，請先執行 main.py" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🚀 正在啟動網頁伺服器..." -ForegroundColor Green
Write-Host ""
Write-Host "📱 請在瀏覽器中開啟以下網址：" -ForegroundColor Cyan
Write-Host "   ➡️  http://127.0.0.1:5000" -ForegroundColor White -BackgroundColor Blue
Write-Host ""
Write-Host "💡 功能說明：" -ForegroundColor Yellow
Write-Host "   • 瀏覽所有生成的四格漫畫腳本" -ForegroundColor White
Write-Host "   • 收聽 AI 生成的語音檔案" -ForegroundColor White
Write-Host "   • 按時間批次查看結果" -ForegroundColor White
Write-Host ""
Write-Host "⛔ 按 Ctrl+C 可停止伺服器" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 設定環境變數
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONLEGACYWINDOWSSTDIO = "utf-8"

# 延遲開啟瀏覽器
Start-Job -ScriptBlock {
    Start-Sleep 3
    Start-Process "http://127.0.0.1:5000"
} | Out-Null

try {
    # 啟動 Flask 應用程式
    python web\app.py
} catch {
    Write-Host ""
    Write-Host "❌ 啟動失敗：$_" -ForegroundColor Red
} finally {
    Write-Host ""
    Write-Host "🛑 伺服器已停止" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "按 Enter 結束"
}
