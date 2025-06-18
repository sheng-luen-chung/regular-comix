# 部署到 GitHub Pages 指南

本指南將幫助您將 Regular Comix 項目部署到 GitHub Pages，讓全世界都能訪問您的 AI 生成四格漫畫。

## 🚀 快速部署步驟

### 1. 設定 GitHub Repository

1. 將您的項目推送到 GitHub
2. 確保 repository 是公開的（GitHub Pages 需要）
3. 前往 Repository 的 **Settings** 頁面

### 2. 設定 GitHub Pages

1. 在 Settings 中找到 **Pages** 選項
2. 在 **Source** 下選擇 "GitHub Actions"
3. 這將啟用 GitHub Actions 進行自動部署

### 3. 設定 API 金鑰

1. 前往 Repository 的 **Settings > Secrets and variables > Actions**
2. 點擊 **New repository secret**
3. 新增以下 secret：
   - **Name**: `GOOGLE_API_KEY`
   - **Value**: 您的 Google AI API 金鑰

### 4. 啟動自動化工作流程

項目包含了完整的 GitHub Actions 工作流程 (`.github/workflows/deploy.yml`)，它會：

- ⏰ 每小時自動執行一次
- 🎭 生成新的漫畫腳本和語音檔案
- 📝 自動提交變更到 repository
- 🚀 自動部署到 GitHub Pages

### 5. 訪問您的網站

部署完成後，您的網站將可以通過以下 URL 訪問：
```
https://YOUR_USERNAME.github.io/regular-comix/
```

## 📁 檔案結構說明

```
regular-comix/
├── .github/workflows/
│   └── deploy.yml              # GitHub Actions 工作流程
├── docs/                       # GitHub Pages 靜態檔案
│   ├── index.html             # 主頁面
│   ├── style.css              # 樣式檔案
│   └── script.js              # JavaScript 功能
├── outputs/                    # 生成的漫畫腳本和語音檔案
├── web/                        # 原始 Flask 應用（本地開發用）
├── main.py                     # 主要生成程式
└── requirements.txt            # Python 依賴
```

## 🛠️ 自訂設定

### 修改執行頻率

編輯 `.github/workflows/deploy.yml` 中的 cron 設定：

```yaml
schedule:
  # 每小時執行 (目前設定)
  - cron: '0 * * * *'
  
  # 每天執行兩次 (早上 8 點和晚上 8 點 UTC)
  # - cron: '0 8,20 * * *'
  
  # 每天執行一次 (UTC 時間早上 9 點)
  # - cron: '0 9 * * *'
```

### 自訂網站外觀

1. 編輯 `docs/style.css` 來修改樣式
2. 編輯 `docs/index.html` 來修改內容
3. 編輯 `docs/script.js` 來修改功能

### 手動觸發生成

1. 前往 GitHub Repository 的 **Actions** 頁面
2. 選擇 "Generate Comics and Deploy" 工作流程
3. 點擊 **Run workflow** 手動執行

## 🔧 故障排除

### 工作流程失敗

1. 檢查 **Actions** 頁面的錯誤日誌
2. 確認 `GOOGLE_API_KEY` secret 設定正確
3. 確認 API 金鑰有足夠的額度

### 網站無法訪問

1. 確認 GitHub Pages 設定正確
2. 檢查 repository 是否為公開
3. 等待 5-10 分鐘讓變更生效

### 內容未更新

1. 檢查最新的 Actions 執行結果
2. 確認 `outputs/` 目錄有新檔案
3. 強制重新整理瀏覽器 (Ctrl+F5)

## 📊 監控和維護

### 查看執行狀態

- **Actions 頁面**: 查看工作流程執行歷史
- **Insights > Traffic**: 查看網站訪問統計
- **Settings > Pages**: 查看部署狀態

### 維護建議

1. 定期檢查 API 使用量
2. 監控 repository 儲存空間
3. 適時清理舊的 outputs 檔案

## 🎯 進階功能

### 添加自訂域名

1. 在 `docs/` 目錄新增 `CNAME` 檔案
2. 檔案內容為您的域名，例如：`comix.example.com`
3. 在域名提供商設定 CNAME 記錄指向 `YOUR_USERNAME.github.io`

### 啟用 HTTPS

GitHub Pages 自動提供 HTTPS，確保在 Pages 設定中啟用 "Enforce HTTPS"。

## 📞 支援

如果您遇到問題：

1. 查看 [GitHub Pages 文檔](https://docs.github.com/en/pages)
2. 查看 [GitHub Actions 文檔](https://docs.github.com/en/actions)
3. 在 repository 中建立 Issue

---

🎉 **恭喜！** 您的 AI 四格漫畫生成器現在已經在 GitHub Pages 上運行了！
