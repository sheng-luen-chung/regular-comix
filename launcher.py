#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regular Comix - 完整啟動工具
包含生成內容、啟動網頁界面、查看結果等功能
"""

import sys
import os
import subprocess
import webbrowser
import time
from pathlib import Path

def setup_encoding():
    """設定 UTF-8 編碼環境"""
    # 設定環境變數
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'
    
    if sys.platform.startswith('win'):
        try:
            # 嘗試設定 Windows 終端機
            os.system('chcp 65001 >nul 2>&1')
            
            # 重新配置標準輸出
            import codecs
            import io
            
            # 使用更安全的方式設定編碼
            if hasattr(sys.stdout, 'buffer'):
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
                sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except Exception as e:
            # 如果失敗，至少確保環境變數已設定
            pass

def show_menu():
    """顯示主選單"""
    print("\n" + "="*60)
    print("🎭 Regular Comix - 四格漫畫腳本與語音產生系統")
    print("="*60)
    print("請選擇要執行的操作：")
    print()
    print("1. 🚀 產生新的漫畫腳本與語音 (main.py)")
    print("2. 🌐 啟動網頁界面查看結果")
    print("3. 📂 開啟結果資料夾")
    print("4. 📊 快速預覽最新結果")
    print("5. 🧹 清理舊檔案")
    print("6. ❌ 退出")
    print()
    
def check_outputs():
    """檢查輸出目錄狀態"""
    outputs_dir = Path("docs/outputs")
    if not outputs_dir.exists():
        print("⚠️  找不到輸出目錄")
        return [], None
    
    batches = [d.name for d in outputs_dir.iterdir() if d.is_dir()]
    batches.sort(reverse=True)
    
    if batches:
        latest = batches[0]
        latest_dir = outputs_dir / latest
        files = list(latest_dir.glob("*.txt"))
        print(f"📊 發現 {len(batches)} 個批次")
        print(f"📅 最新批次：{latest} ({len(files)} 個腳本)")
        return batches, latest
    else:
        print("📭 尚無生成結果")
        return [], None

def generate_content():
    """生成新內容"""
    print("\n🚀 開始生成新的漫畫腳本與語音...")
    print("這可能需要幾分鐘時間，請耐心等待...")
    print("="*50)
    
    try:
        result = subprocess.run([sys.executable, "main.py"], 
                              capture_output=False, text=True)
        if result.returncode == 0:
            print("\n✅ 生成完成！")
        else:
            print(f"\n❌ 生成失敗，返回代碼：{result.returncode}")
    except Exception as e:
        print(f"\n❌ 執行錯誤：{e}")
    
    input("\n按 Enter 繼續...")

def start_web():
    """啟動網頁界面"""
    print("\n🌐 啟動網頁界面...")
    
    if not Path("web/app.py").exists():
        print("❌ 找不到 web/app.py")
        input("按 Enter 繼續...")
        return
    
    print("📱 網址：http://127.0.0.1:5000")
    print("⛔ 按 Ctrl+C 停止伺服器")
    print("="*50)
    
    # 3秒後開啟瀏覽器
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open('http://127.0.0.1:5000')
            print("🌐 瀏覽器已開啟")
        except:
            pass
    
    import threading
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        subprocess.run([sys.executable, "web/app.py"])
    except KeyboardInterrupt:
        print("\n👋 伺服器已停止")
    except Exception as e:
        print(f"\n❌ 啟動失敗：{e}")
    
    input("\n按 Enter 繼續...")

def open_folder():
    """開啟結果資料夾"""
    outputs_dir = Path("docs/outputs")
    if not outputs_dir.exists():
        print("❌ 找不到輸出目錄")
        input("按 Enter 繼續...")
        return
    
    try:
        if sys.platform.startswith('win'):
            os.startfile(str(outputs_dir))
        elif sys.platform.startswith('darwin'):
            subprocess.run(['open', str(outputs_dir)])
        else:
            subprocess.run(['xdg-open', str(outputs_dir)])
        print("📂 已開啟結果資料夾")
    except Exception as e:
        print(f"❌ 無法開啟資料夾：{e}")
    
    input("按 Enter 繼續...")

def quick_preview():
    """快速預覽最新結果"""
    batches, latest = check_outputs()
    if not latest:
        print("📭 沒有結果可預覽")
        input("按 Enter 繼續...")
        return
    
    try:
        subprocess.run([sys.executable, "quick_preview.py"])
    except Exception as e:
        print(f"❌ 預覽失敗：{e}")
    
    input("按 Enter 繼續...")

def cleanup():
    """清理舊檔案"""
    print("\n🧹 清理功能")
    print("這將刪除超過 30 天的舊結果檔案")
    confirm = input("確定要繼續嗎？(y/N): ")
    
    if confirm.lower() == 'y':
        try:
            subprocess.run([sys.executable, "-c", """
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

outputs_dir = Path('docs/outputs')
if outputs_dir.exists():
    cutoff = datetime.now() - timedelta(days=30)
    deleted = 0
    for batch_dir in outputs_dir.iterdir():
        if batch_dir.is_dir():
            try:
                # 解析日期 (YYYYMMDD_HHMM)
                date_str = batch_dir.name[:8]
                batch_date = datetime.strptime(date_str, '%Y%m%d')
                if batch_date < cutoff:
                    shutil.rmtree(batch_dir)
                    deleted += 1
                    print(f'Deleted: {batch_dir.name}')
            except:
                pass
    print(f'清理完成，刪除了 {deleted} 個舊批次')
else:
    print('找不到輸出目錄')
"""])
        except Exception as e:
            print(f"❌ 清理失敗：{e}")
    else:
        print("已取消清理")
    
    input("按 Enter 繼續...")

def main():
    """主程式"""
    setup_encoding()
    
    while True:
        try:
            # 清除螢幕（跨平台）
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # 顯示狀態
            check_outputs()
            
            # 顯示選單
            show_menu()
            
            choice = input("請選擇 (1-6): ").strip()
            
            if choice == '1':
                generate_content()
            elif choice == '2':
                start_web()
            elif choice == '3':
                open_folder()
            elif choice == '4':
                quick_preview()
            elif choice == '5':
                cleanup()
            elif choice == '6':
                print("\n👋 再見！")
                break
            else:
                print("\n❌ 無效選擇，請重新選擇")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n👋 程式已中斷")
            break
        except Exception as e:
            print(f"\n❌ 發生錯誤：{e}")
            input("按 Enter 繼續...")

if __name__ == '__main__':
    main()
