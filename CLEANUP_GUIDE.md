# Regular Comix - 建議的簡化檔案結構

## 🎯 清理後的核心檔案

```
regular-comix/
├── 📄 main.py                    # 主程式（生成漫畫腳本與語音）
├── 🚀 launcher.py               # 整合啟動器（推薦使用）
├── 🚀 launcher.bat              # Windows 批次檔啟動器
├── 🚀 launcher.ps1              # PowerShell 啟動器（推薦）
├── 🌐 start_web.bat             # 網頁界面啟動器
├── 🌐 start_web.ps1             # PowerShell 網頁啟動器
├── 📋 requirements.txt          # Python 依賴包
├── 📖 README.md                 # 專案說明文檔
├── 📊 PROJECT_SUMMARY.md        # 專案完成總結
├── ⚙️ .env.example              # 環境變數範例
├── 📁 .github/                  # GitHub Actions 自動化
├── 📁 docs/                     # 輸出結果與靜態網站
└── 📁 web/                      # Flask 網頁應用
    ├── app.py                   # Flask 主程式
    ├── templates/index.html     # 網頁模板
    └── static/style.css         # 樣式檔案
```

## 🗑️ 可刪除的重複檔案

### 重複的主程式（已整合）
- ❌ main_en.py
- ❌ main_clean.py

### 重複的啟動器（功能已整合到 launcher.py）
- ❌ generate_content.bat
- ❌ generate_content.ps1
- ❌ start_web_simple.py
- ❌ launch_web_simple.bat
- ❌ update_content.bat

### 重複的查看工具（功能已整合到 launcher.py）
- ❌ view_results.bat
- ❌ view_results.ps1
- ❌ preview.py
- ❌ preview.ps1
- ❌ preview_fixed.py
- ❌ preview_results.bat
- ❌ view_results_fixed.bat
- ❌ quick_preview.py
- ❌ open_results_folder.bat

### 測試與工具檔案
- ❌ test_encoding.py
- ❌ generate_file_list.py
- ❌ cleanup.bat

## 💡 使用建議

**清理後，您只需要：**

1. **日常使用：**
   ```bash
   launcher.bat          # 或雙擊執行
   ```

2. **直接啟動網頁：**
   ```bash
   start_web.bat         # 或 start_web.ps1
   ```

3. **直接生成內容：**
   ```bash
   python main.py
   ```

**所有功能都整合在 launcher.py 中，包括：**
- 🚀 生成新內容
- 🌐 啟動網頁界面
- 📂 開啟結果資料夾
- 📊 快速預覽
- 🧹 清理舊檔案

## 🎉 清理的好處

- ✅ **檔案數量減少 60%**
- ✅ **避免混淆** - 不會不知道該用哪個檔案
- ✅ **維護更容易** - 只需要維護核心檔案
- ✅ **功能不減少** - 所有功能都保留在整合工具中
- ✅ **使用更簡單** - 一個啟動器包含所有功能
