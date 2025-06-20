import os
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
import sys

# Fix Windows console encoding issues
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if not GOOGLE_API_KEY:
    print("錯誤: 未找到 GOOGLE_API_KEY 環境變數")
    sys.exit(1)

genai.configure(api_key=GOOGLE_API_KEY)

OUTPUT_DIR = 'docs/outputs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_top_news(num_topics=5, max_retries=3):
    url = 'https://news.google.com/rss?hl=zh-TW&gl=TW&ceid=TW:zh-TW'
    
    for attempt in range(max_retries):
        try:
            print(f"嘗試獲取新聞 (第 {attempt + 1} 次)...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')
            
            if not items:
                print("警告: 未找到新聞項目")
                continue
                
            topics = []
            seen = set()
            for item in items:
                title = item.title.text.strip()
                # 以標題的主題詞去重
                topic = title.split('：')[-1] if '：' in title else title
                if topic not in seen and len(topic) > 5:  # 過濾太短的標題
                    seen.add(topic)
                    topics.append(topic)
                if len(topics) >= num_topics:
                    break
                    
            if topics:
                print(f"✓ 成功獲取 {len(topics)} 個新聞主題")
                return topics
            else:
                print("警告: 未找到有效的新聞主題")
                
        except requests.exceptions.RequestException as e:
            print(f"✗ 網路請求失敗 (第 {attempt + 1} 次): {str(e)}")
            if attempt < max_retries - 1:
                print("等待 5 秒後重試...")
                import time
                time.sleep(5)
            else:
                print("已達到最大重試次數")
                
        except Exception as e:
            print(f"✗ 解析新聞時發生錯誤: {str(e)}")
            break
            
    return []

def generate_comic_script(topic, max_retries=3):
    prompt = f"""
    根據這個主題：{topic}
    請用幽默的方式，創作一個四格漫畫腳本（中文），每格包含：
    1. 場景描述
    2. 角色動作
    3. 對話（如有）
    輸出格式：
    第一格：\n[描述]\n
    第二格：\n[描述]\n
    第三格：\n[描述]\n
    第四格：\n[描述]\n
    """
    
    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel(model_name='models/gemini-2.0-flash')
            response = model.generate_content(prompt)
            
            if response.text and response.text.strip():
                return response.text.strip()
            else:
                print(f"✗ API 回應為空 (第 {attempt + 1} 次)")
                
        except Exception as e:
            print(f"✗ 生成腳本失敗 (第 {attempt + 1} 次): {str(e)}")
            if attempt < max_retries - 1:
                import time
                time.sleep(2)
                
    raise Exception("無法生成漫畫腳本")

def save_script_and_voice(topic, script, timestamp):
    import re
    # 建立批次資料夾
    batch_dir = os.path.join(OUTPUT_DIR, timestamp)
    os.makedirs(batch_dir, exist_ok=True)
    # 移除 Windows 不允許的檔名字元
    safe_topic = re.sub(r'[\\/:*?"<>|\s]', '_', topic)[:20]
    base = os.path.join(batch_dir, safe_topic)
    script_path = f"{base}.txt"
    voice_path = f"{base}.mp3"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script)
    tts = gTTS(script, lang='zh-tw')
    tts.save(voice_path)
    return script_path, voice_path

def main():
    try:
        now = datetime.now().strftime('%Y%m%d_%H%M')
        print(f"開始生成漫畫腳本 - {now}")
        
        topics = get_top_news(num_topics=5)
        if not topics:
            print("警告: 未找到新聞主題")
            return
            
        print(f"找到 {len(topics)} 個新聞主題")
        
        for idx, topic in enumerate(topics, 1):
            print(f"\n處理主題 {idx}/{len(topics)}: {topic}")
            try:
                script = generate_comic_script(topic)
                print(f"✓ 已生成漫畫腳本")
                
                script_path, voice_path = save_script_and_voice(topic, script, now)
                print(f"✓ 已儲存：{script_path} 和 {voice_path}")
                
            except Exception as e:
                print(f"✗ 處理主題 '{topic}' 時發生錯誤: {str(e)}")
                continue
                
        print(f"\n✓ 完成所有任務")
        
    except Exception as e:
        print(f"✗ 執行過程中發生錯誤: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
