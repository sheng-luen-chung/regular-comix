#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regular Comix - 專案清理工具
刪除不必要的重複檔案，保留核心功能
"""

import os
import sys
from pathlib import Path

# 建議刪除的檔案列表
FILES_TO_DELETE = [
    # 重複的主程式
    "main_en.py",
    "main_clean.py",
    
    # 重複的啟動器
    "generate_content.bat",
    "generate_content.ps1", 
    "start_web_simple.py",
    "launch_web_simple.bat",
    "update_content.bat",
    
    # 重複的查看工具
    "view_results.bat",
    "view_results.ps1",
    "preview.py",
    "preview.ps1", 
    "preview_fixed.py",
    "preview_results.bat",
    "view_results_fixed.bat",
    "quick_preview.py",
    "open_results_folder.bat",
    
    # 測試/工具檔案
    "test_encoding.py",
    "generate_file_list.py",
    "cleanup.bat",
]

# 核心保留檔案（供參考）
CORE_FILES = [
    "main.py",              # 主程式
    "launcher.py",          # 整合啟動器
    "launcher.bat",         # Windows 批次檔
    "launcher.ps1",         # PowerShell 腳本
    "start_web.bat",        # 網頁啟動器
    "start_web.ps1",        # PowerShell 網頁啟動器
    "requirements.txt",     # Python 依賴
    "README.md",           # 說明文檔
    "PROJECT_SUMMARY.md",  # 專案總結
    ".env.example",        # 環境變數範例
]

def setup_encoding():
    """設定 UTF-8 編碼"""
    if sys.platform.startswith('win'):
        try:
            os.system('chcp 65001 >nul 2>&1')
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        except:
            pass

def main():
    setup_encoding()
    
    print("🧹 Regular Comix 專案清理工具")
    print("=" * 50)
    print()
    
    # 檢查要刪除的檔案
    existing_files = []
    for filename in FILES_TO_DELETE:
        if os.path.exists(filename):
            existing_files.append(filename)
    
    if not existing_files:
        print("✅ 沒有需要清理的檔案")
        input("按 Enter 結束...")
        return
    
    print(f"📋 發現 {len(existing_files)} 個可清理的檔案：")
    print()
    
    for i, filename in enumerate(existing_files, 1):
        print(f"   {i:2d}. {filename}")
    
    print()
    print("💡 這些檔案的功能已整合到 launcher.py 中")
    print("🎯 清理後將保留以下核心檔案：")
    print()
    
    for filename in CORE_FILES:
        if os.path.exists(filename):
            print(f"   ✅ {filename}")
    
    print()
    print("⚠️  這個操作無法復原！")
    confirm = input("確定要刪除這些檔案嗎？(y/N): ")
    
    if confirm.lower() == 'y':
        deleted_count = 0
        for filename in existing_files:
            try:
                os.remove(filename)
                print(f"🗑️  已刪除：{filename}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ 刪除失敗：{filename} - {e}")
        
        print()
        print(f"✅ 清理完成！已刪除 {deleted_count} 個檔案")
        print()
        print("🎉 現在您的專案更簡潔了！")
        print("💡 請使用以下命令啟動：")
        print("   • launcher.bat (Windows)")
        print("   • launcher.ps1 (PowerShell)")
        print("   • python launcher.py (跨平台)")
        
    else:
        print("❌ 已取消清理")
    
    print()
    input("按 Enter 結束...")

if __name__ == '__main__':
    main()
