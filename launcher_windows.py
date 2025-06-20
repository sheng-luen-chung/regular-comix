#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regular Comix - Windows 友善啟動器
專門針對 Windows 中文顯示優化
"""

import sys
import os
import subprocess
import time
from pathlib import Path

def setup_windows_encoding():
    """Windows 特別編碼設定"""
    if not sys.platform.startswith('win'):
        return
    
    try:
        # 強制設定 Windows 終端機
        os.system('chcp 65001 >nul 2>&1')
        
        # 設定環境變數
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        os.environ['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'
        
        # 嘗試重新配置輸出
        import io
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout = io.TextIOWrapper(
                sys.stdout.buffer, 
                encoding='utf-8', 
                errors='replace',
                newline='\n'
            )
            sys.stderr = io.TextIOWrapper(
                sys.stderr.buffer, 
                encoding='utf-8', 
                errors='replace',
                newline='\n'
            )
    except:
        pass

def safe_print(text):
    """安全的中文輸出"""
    try:
        print(text)
    except UnicodeEncodeError:
        # 如果還是有問題，就使用 ASCII 版本
        ascii_text = text.encode('ascii', 'replace').decode('ascii')
        print(ascii_text)

def show_menu():
    """顯示主選單（Windows 優化版）"""
    safe_print("\n" + "="*50)
    safe_print("🎭 Regular Comix - 四格漫畫腳本與語音產生系統")
    safe_print("="*50)
    safe_print("請選擇要執行的操作：")
    safe_print("")
    safe_print("1. 🚀 產生新的漫畫腳本與語音")
    safe_print("2. 🌐 啟動網頁界面查看結果")
    safe_print("3. 📂 開啟結果資料夾")
    safe_print("4. 📊 快速預覽最新結果")
    safe_print("5. 🧹 清理舊檔案")
    safe_print("6. ❌ 退出")
    safe_print("")

def check_outputs():
    """檢查輸出目錄狀態"""
    outputs_dir = Path("docs/outputs")
    if not outputs_dir.exists():
        safe_print("⚠️  找不到輸出目錄")
        return [], None
    
    batches = [d.name for d in outputs_dir.iterdir() if d.is_dir()]
    batches.sort(reverse=True)
    
    if batches:
        latest = batches[0]
        latest_dir = outputs_dir / latest
        files = list(latest_dir.glob("*.txt"))
        safe_print(f"📊 發現 {len(batches)} 個批次")
        safe_print(f"📅 最新批次：{latest} ({len(files)} 個腳本)")
        return batches, latest
    else:
        safe_print("📭 尚無生成結果")
        return [], None

def generate_content():
    """生成新內容"""
    safe_print("\n🚀 開始生成新的漫畫腳本與語音...")
    safe_print("這可能需要幾分鐘時間，請耐心等待...")
    safe_print("="*40)
    
    try:
        result = subprocess.run([sys.executable, "main.py"], 
                              capture_output=False, text=True)
        if result.returncode == 0:
            safe_print("\n✅ 生成完成！")
        else:
            safe_print(f"\n❌ 生成失敗，返回代碼：{result.returncode}")
    except Exception as e:
        safe_print(f"\n❌ 執行錯誤：{e}")
    
    input("\n按 Enter 繼續...")

def start_web():
    """啟動網頁界面"""
    safe_print("\n🌐 啟動網頁界面...")
    
    # 優先使用 PowerShell 腳本
    if Path("start_web.ps1").exists():
        try:
            safe_print("使用 PowerShell 啟動器...")
            subprocess.run([
                "powershell.exe", 
                "-ExecutionPolicy", "Bypass", 
                "-File", "start_web.ps1"
            ])
            return
        except:
            pass
    
    # 備用方案：直接啟動 Flask
    if not Path("web/app.py").exists():
        safe_print("❌ 找不到 web/app.py")
        input("按 Enter 繼續...")
        return
    
    safe_print("📱 網址：http://127.0.0.1:5000")
    safe_print("⛔ 按 Ctrl+C 停止伺服器")
    safe_print("="*40)
    
    try:
        subprocess.run([sys.executable, "web/app.py"])
    except KeyboardInterrupt:
        safe_print("\n👋 伺服器已停止")
    except Exception as e:
        safe_print(f"\n❌ 啟動失敗：{e}")
    
    input("\n按 Enter 繼續...")

def open_folder():
    """開啟結果資料夾"""
    outputs_dir = Path("docs/outputs")
    if not outputs_dir.exists():
        safe_print("❌ 找不到輸出目錄")
        input("按 Enter 繼續...")
        return
    
    try:
        os.startfile(str(outputs_dir))
        safe_print("📂 已開啟結果資料夾")
    except Exception as e:
        safe_print(f"❌ 無法開啟資料夾：{e}")
    
    input("按 Enter 繼續...")

def quick_preview():
    """快速預覽最新結果"""
    outputs_dir = Path("docs/outputs")
    if not outputs_dir.exists():
        safe_print("📭 沒有結果可預覽")
        input("按 Enter 繼續...")
        return
    
    batches = [d.name for d in outputs_dir.iterdir() if d.is_dir()]
    if not batches:
        safe_print("📭 沒有結果可預覽")
        input("按 Enter 繼續...")
        return
    
    latest = sorted(batches, reverse=True)[0]
    latest_dir = outputs_dir / latest
    files = list(latest_dir.glob("*.txt"))
    
    safe_print(f"📅 最新批次：{latest}")
    safe_print(f"📄 腳本數量：{len(files)}")
    safe_print("📝 腳本標題：")
    
    for i, file in enumerate(files[:5], 1):
        title = file.stem
        # 嘗試安全顯示標題
        try:
            safe_print(f"   {i}. {title}")
        except:
            safe_print(f"   {i}. [Script {i}]")
    
    if len(files) > 5:
        safe_print(f"   ... 還有 {len(files) - 5} 個腳本")
    
    input("\n按 Enter 繼續...")

def cleanup():
    """清理舊檔案"""
    safe_print("\n🧹 清理功能")
    safe_print("這將刪除超過 30 天的舊結果檔案")
    confirm = input("確定要繼續嗎？(y/N): ")
    
    if confirm.lower() == 'y':
        try:
            from datetime import datetime, timedelta
            import shutil
            
            outputs_dir = Path('docs/outputs')
            if outputs_dir.exists():
                cutoff = datetime.now() - timedelta(days=30)
                deleted = 0
                for batch_dir in outputs_dir.iterdir():
                    if batch_dir.is_dir():
                        try:
                            date_str = batch_dir.name[:8]
                            batch_date = datetime.strptime(date_str, '%Y%m%d')
                            if batch_date < cutoff:
                                shutil.rmtree(batch_dir)
                                deleted += 1
                        except:
                            pass
                safe_print(f'✅ 清理完成，刪除了 {deleted} 個舊批次')
            else:
                safe_print('❌ 找不到輸出目錄')
        except Exception as e:
            safe_print(f"❌ 清理失敗：{e}")
    else:
        safe_print("已取消清理")
    
    input("按 Enter 繼續...")

def main():
    """主程式"""
    setup_windows_encoding()
    
    while True:
        try:
            # 清除螢幕
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
                safe_print("\n👋 再見！")
                break
            else:
                safe_print("\n❌ 無效選擇，請重新選擇")
                time.sleep(1)
                
        except KeyboardInterrupt:
            safe_print("\n\n👋 程式已中斷")
            break
        except Exception as e:
            safe_print(f"\n❌ 發生錯誤：{e}")
            input("按 Enter 繼續...")

if __name__ == '__main__':
    main()
