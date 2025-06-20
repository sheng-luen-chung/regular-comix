@echo off
chcp 65001 >nul
echo [START] 開始生成最新的四格漫畫內容...
echo.

echo [STEP 1] 獲取最新新聞並生成四格漫畫
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] 生成四格漫畫時發生錯誤
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [STEP 2] 更新檔案清單
python generate_file_list.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] 更新檔案清單時發生錯誤
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [SUCCESS] 完成！您現在可以在瀏覽器中查看最新的內容了
echo [TIP] 請在 VS Code 中開啟 docs/index.html 並使用 Live Server
echo.
pause
