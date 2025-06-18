# Regular Comix

自動從 Google News 擷取新聞主題，產生四格漫畫腳本並以語音播報。使用 GitHub Actions 每小時自動執行。

## 功能特色

- 📰 自動從 Google News RSS 擷取熱門新聞
- 🎭 使用 Google Gemini AI 生成幽默的四格漫畫腳本
- 🔊 將腳本轉換為中文語音檔案
- ⏰ 每小時自動執行（透過 GitHub Actions）
- 📁 自動保存結果到 `outputs/` 目錄

## 設定指南

### 1. 設定 Google AI API 金鑰

1. 前往 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 建立新的 API 金鑰
3. 在 GitHub 專案的 Settings > Secrets and variables > Actions 中
4. 新增 Repository secret：
   - Name: `GOOGLE_API_KEY`
   - Value: 你的 API 金鑰

### 2. 啟用 GitHub Actions

GitHub Actions 工作流程會自動：
- 每小時執行一次
- 生成新的漫畫腳本和語音檔案
- 自動提交並推送到 repository

### 3. 手動執行

你也可以在 GitHub 的 Actions 頁面手動觸發工作流程。

## 本地開發

1. 克隆專案：
```bash
git clone <your-repo-url>
cd regular-comix
```

2. 安裝依賴：
```bash
pip install -r requirements.txt
```

3. 設定環境變數：
```bash
# 建立 .env 檔案
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

4. 執行程式：
```bash
python main.py
```

## 檔案結構

```
regular-comix/
├── .github/workflows/auto-update.yml  # GitHub Actions 工作流程
├── main.py                           # 主程式
├── requirements.txt                   # Python 依賴
├── outputs/                          # 生成的檔案
│   └── YYYYMMDD_HHMM/               # 按時間戳分組
│       ├── *.txt                    # 漫畫腳本
│       └── *.mp3                    # 語音檔案
└── web/                             # Web 介面（可選）
```

## 技術棧

- **Python 3.11+**
- **Google Generative AI (Gemini)** - 生成漫畫腳本
- **Google Text-to-Speech (gTTS)** - 語音合成
- **Beautiful Soup** - RSS 解析
- **GitHub Actions** - 自動化執行
