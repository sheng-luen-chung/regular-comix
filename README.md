# Regular Comix

自動從 Google News 擷取新聞主題，產生四格漫畫腳本並以語音播報。使用 GitHub Actions 每小時自動執行，並部署到 GitHub Pages。

## 🌐 線上預覽

**[🎭 訪問 Regular Comix 網站](https://YOUR_USERNAME.github.io/regular-comix/)**

## 功能特色

- 📰 自動從 Google News RSS 擷取熱門新聞
- 🎭 使用 Google Gemini AI 生成幽默的四格漫畫腳本
- 🔊 將腳本轉換為中文語音檔案
- ⏰ 每小時自動執行（透過 GitHub Actions）
- 📁 自動保存結果到 `outputs/` 目錄
- 🚀 自動部署到 GitHub Pages
- 📱 響應式網頁設計，支援手機和桌面

## 快速開始

### 🚀 部署到 GitHub Pages

1. **Fork 或複製此 repository**
2. **設定 API 金鑰**: 在 Repository Settings > Secrets 中新增 `GOOGLE_API_KEY`
3. **啟用 GitHub Pages**: 在 Settings > Pages 中選擇 "GitHub Actions"
4. **等待自動部署**: GitHub Actions 會自動生成內容並部署

詳細部署指南請參考 [DEPLOY.md](DEPLOY.md)

### 🛠️ 本地開發

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

## 🔄 本地端查看新生成的結果

當您在本地端生成新的四格漫畫後，有兩種方法可以立即查看 `docs/outputs/` 底下的新結果：

### 方法 1：靜態網站 + Live Server（推薦）

**步驟 1: 更新內容**
```bash
# 一鍵更新所有內容（生成新腳本 + 更新檔案清單）
./update_content.bat

# 或分別執行：
python main.py                    # 生成新的四格漫畫腳本
python generate_file_list.py      # 更新檔案清單
```

**步驟 2: 查看結果**
- 在 VS Code 中開啟 `docs/index.html`
- 右鍵選擇 "Open with Live Server"
- 選擇最新的時間批次查看新內容

### 方法 2：動態網站 Flask 應用

**啟動 Flask 服務器**
```bash
./start_web.bat
# 或手動執行：
cd web && python app.py
```

**查看結果**
- 瀏覽器打開 `http://127.0.0.1:5000`
- 自動掃描所有檔案，無需手動更新檔案清單

### 🎯 方法比較

| 特點 | 靜態網站 (方法 1) | 動態網站 (方法 2) |
|------|------------------|------------------|
| **設定難度** | 簡單 | 簡單 |
| **檔案更新** | 需執行 `generate_file_list.py` | 自動掃描檔案 |
| **依賴** | VS Code Live Server | Flask |
| **效能** | 快速 | 稍慢 |
| **推薦度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 檔案結構

```
regular-comix/
├── .github/workflows/
│   └── regular-comix.yml        # GitHub Actions 自動執行工作流程
├── docs/                        # GitHub Pages 靜態網站檔案
│   ├── index.html              # 網站主頁
│   ├── style.css               # 網站樣式
│   ├── script.js               # 網站功能
│   └── outputs/                # 生成的檔案（GitHub Pages 可直接存取）
│       └── YYYYMMDD_HHMM/      # 按時間戳分組
│           ├── *.txt           # 漫畫腳本
│           └── *.mp3           # 語音檔案
├── main.py                      # 主程式
├── generate_file_list.py        # 生成檔案清單工具
├── update_content.bat           # 一鍵更新腳本（Windows）
├── start_web.bat               # 啟動 Flask 網站（Windows）
├── requirements.txt             # Python 依賴
├── DEPLOY.md                    # 部署指南
└── web/                        # 本地開發用 Flask 應用
    ├── app.py                  # Flask 後端
    ├── templates/
    └── static/
```

## 技術棧

- **Python 3.11+**
- **Google Generative AI (Gemini)** - 生成漫畫腳本
- **Google Text-to-Speech (gTTS)** - 語音合成
- **Beautiful Soup** - RSS 解析
- **GitHub Actions** - 自動化執行和部署
- **GitHub Pages** - 靜態網站託管
- **HTML/CSS/JavaScript** - 前端網頁介面

## 🎯 使用說明

### 線上使用

1. 訪問 [GitHub Pages 網站](https://YOUR_USERNAME.github.io/regular-comix/)
2. 選擇想要查看的生成批次
3. 閱讀漫畫腳本
4. 播放或下載語音檔案

### 本地開發

參考上方的「本地開發」章節設定。

## 📈 監控和維護

- **執行狀態**: 查看 GitHub Actions 頁面
- **網站流量**: 查看 GitHub Insights
- **API 使用量**: 監控 Google AI API 額度

## 🤝 貢獻

歡迎提交 Pull Request 或建立 Issue 來改善這個項目！

## 📄 授權

MIT License - 詳見 [LICENSE](LICENSE) 檔案
