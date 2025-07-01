import os
import json
import subprocess
import sys
from datetime import datetime

def generate_file_list():
    """生成 file-list.json，掃描 docs/outputs/ 下的實際內容"""
    
    outputs_dir = 'docs/outputs'
    file_list = {}
    
    if not os.path.exists(outputs_dir):
        print(f"❌ 目錄不存在: {outputs_dir}")
        return False
    
    print(f"📁 掃描目錄: {outputs_dir}")
    
    # 掃描所有批次目錄
    batch_count = 0
    for batch_name in sorted(os.listdir(outputs_dir), reverse=True):  # 按時間排序，最新在前
        batch_path = os.path.join(outputs_dir, batch_name)
        
        if not os.path.isdir(batch_path):
            continue
            
        batch_files = []
        txt_files = [f for f in os.listdir(batch_path) if f.endswith('.txt')]
        
        for txt_file in sorted(txt_files):  # 按檔名排序
            name = txt_file[:-4]  # 移除 .txt 副檔名
            mp3_file = f"{name}.mp3"
            mp3_path = os.path.join(batch_path, mp3_file)
            
            file_info = {
                "name": name,
                "txt": txt_file,
                "mp3": mp3_file if os.path.exists(mp3_path) else None
            }
            
            batch_files.append(file_info)
        
        # 只添加有檔案的批次
        if batch_files:
            file_list[batch_name] = batch_files
            batch_count += 1
            print(f"✅ 批次 {batch_name}: {len(batch_files)} 個檔案")
        else:
            print(f"⚠️  批次 {batch_name}: 沒有檔案，跳過")
    
    # 寫入 JSON 檔案
    output_file = 'docs/file-list.json'
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(file_list, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 已生成 {output_file}")
        print(f"📊 總共包含 {batch_count} 個有內容的批次")
        return True
    except Exception as e:
        print(f"❌ 寫入檔案失敗: {e}")
        return False

def sync_to_github():
    """同步本地更改到 GitHub"""
    try:
        print(f"\n🔄 開始同步到 GitHub...")
        
        # 檢查 git status
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if not result.stdout.strip():
            print(f"ℹ️  沒有檔案需要提交")
            return True
        
        print(f"📝 發現需要提交的檔案:")
        print(result.stdout)
        
        # 添加所有更改
        subprocess.run(['git', 'add', '.'], check=True)
        print(f"✅ 已添加檔案到 git")
        
        # 提交更改
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commit_msg = f"📝 手動更新漫畫內容 - {timestamp}"
        
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        print(f"✅ 已提交更改: {commit_msg}")
        
        # 推送到 GitHub
        subprocess.run(['git', 'push'], check=True)
        print(f"🚀 已推送到 GitHub")
        
        print(f"\n🎉 同步完成！")
        print(f"🌐 請等待 2-5 分鐘，GitHub Pages 會自動更新")
        print(f"📱 您可以在 GitHub Pages 網站上看到最新內容")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 操作失敗: {e}")
        return False
    except Exception as e:
        print(f"❌ 同步過程發生錯誤: {e}")
        return False

def main():
    """主函數：更新文件列表並同步到 GitHub"""
    print(f"🚀 Regular Comix 內容同步工具")
    print(f"{'='*50}")
    
    # 1. 更新檔案列表
    if not generate_file_list():
        print(f"❌ 文件列表更新失敗")
        sys.exit(1)
    
    # 2. 詢問是否要同步到 GitHub
    try:
        sync_choice = input(f"\n🤔 是否要將更改同步到 GitHub Pages？(y/N): ").lower().strip()
        
        if sync_choice in ['y', 'yes', '是']:
            if sync_to_github():
                print(f"\n✨ 所有操作完成！")
            else:
                print(f"\n❌ 同步失敗，請檢查網絡連接和 git 設定")
                sys.exit(1)
        else:
            print(f"\nℹ️  僅更新了本地文件列表")
            print(f"💡 如需同步到 GitHub Pages，請稍後執行:")
            print(f"   git add . && git commit -m '更新內容' && git push")
            
    except KeyboardInterrupt:
        print(f"\n\n👋 操作已取消")
        sys.exit(0)

if __name__ == '__main__':
    main()
