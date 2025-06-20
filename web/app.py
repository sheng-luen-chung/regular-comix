from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs', 'outputs')

def get_batches():
    """取得所有批次資料夾（依時間排序）"""
    try:
        if not os.path.exists(OUTPUTS_DIR):
            return []
        batches = [d for d in os.listdir(OUTPUTS_DIR) 
                  if os.path.isdir(os.path.join(OUTPUTS_DIR, d))]
        return sorted(batches, reverse=True)
    except Exception as e:
        print(f"Error getting batches: {e}")
        return []

def get_scripts(batch):
    """取得指定批次的所有腳本"""
    if not batch:
        return []
    
    try:
        batch_dir = os.path.join(OUTPUTS_DIR, batch)
        if not os.path.exists(batch_dir):
            return []
            
        scripts = []
        for fname in sorted(os.listdir(batch_dir)):
            if fname.endswith('.txt'):
                topic = fname[:-4]  # 移除 .txt 副檔名
                txt_path = os.path.join(batch_dir, fname)
                mp3_path = os.path.join(batch_dir, topic + '.mp3')
                  # 讀取腳本內容
                try:
                    with open(txt_path, encoding='utf-8') as f:
                        content = f.read()
                    # 確保內容不為空且適合顯示
                    text = content.strip() if content.strip() else "腳本內容讀取中..."
                except UnicodeDecodeError:
                    # 嘗試其他編碼
                    try:
                        with open(txt_path, encoding='big5') as f:
                            content = f.read()
                        text = content.strip() if content.strip() else "腳本內容讀取中..."
                    except:
                        text = "無法讀取腳本內容（編碼問題）"
                except Exception as e:
                    print(f"Error reading {txt_path}: {e}")
                    text = f"讀取錯誤：{str(e)}"
                
                # 檢查對應的 MP3 檔案是否存在
                mp3_exists = os.path.exists(mp3_path)
                
                scripts.append({
                    'topic': topic,
                    'text': text,
                    'txt': fname,
                    'mp3': topic + '.mp3' if mp3_exists else None
                })
        return scripts
    except Exception as e:
        print(f"Error getting scripts for batch {batch}: {e}")
        return []

@app.route('/')
def index():
    """首頁 - 顯示最新批次的腳本"""
    batches = get_batches()
    latest = batches[0] if batches else None
    scripts = get_scripts(latest) if latest else []
    return render_template('index.html', 
                         batches=batches, 
                         current_batch=latest, 
                         scripts=scripts)

@app.route('/batch/<batch>')
def batch(batch):
    """顯示指定批次的腳本"""
    batches = get_batches()
    scripts = get_scripts(batch)
    return render_template('index.html', 
                         batches=batches, 
                         current_batch=batch, 
                         scripts=scripts)

@app.route('/outputs/<batch>/<filename>')
def download_file(batch, filename):
    """下載檔案"""
    try:
        batch_dir = os.path.join(OUTPUTS_DIR, batch)
        return send_from_directory(batch_dir, filename)
    except Exception as e:
        print(f"Error serving file {filename}: {e}")
        return "檔案不存在", 404

if __name__ == '__main__':
    import sys
    import codecs
    import os
    
    # 設定環境變數確保 UTF-8 輸出
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'
    
    # 設定 stdout 編碼為 UTF-8（Windows 相容）
    if sys.platform.startswith('win'):
        try:
            # 嘗試設定 Windows 終端機為 UTF-8
            os.system('chcp 65001 >nul 2>&1')
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
        except:
            pass  # 如果失敗就使用預設編碼
    
    print("🚀 啟動 Regular Comix 網頁界面...")
    print(f"📁 輸出目錄：{OUTPUTS_DIR}")
    
    # 檢查 outputs 目錄
    if not os.path.exists(OUTPUTS_DIR):
        print("⚠️  警告：找不到輸出目錄，請先執行 main.py 產生內容")
    else:
        batches = get_batches()
        print(f"📊 發現 {len(batches)} 個批次")
        if batches:
            print(f"📅 最新批次：{batches[0]}")
    
    print("🌐 請在瀏覽器開啟：http://127.0.0.1:5000")
    print("⛔ 按 Ctrl+C 停止伺服器")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='127.0.0.1', port=5000)
    except KeyboardInterrupt:
        print("\n👋 伺服器已停止")
    