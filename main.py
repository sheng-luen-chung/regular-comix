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
            print(f"🌐 嘗試獲取新聞 (第 {attempt + 1}/{max_retries} 次)...")
            print(f"📡 連接到 Google News RSS...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            print(f"✅ 網絡請求成功！")
            
            print(f"📄 正在解析 RSS 內容...")
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')
            
            if not items:
                print("⚠️ 未找到新聞項目")
                continue
                
            print(f"📰 找到 {len(items)} 個新聞項目，正在篩選...")
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
                print(f"✅ 成功篩選出 {len(topics)} 個優質新聞主題")
                return topics
            else:
                print("⚠️ 未找到有效的新聞主題")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 網路請求失敗 (第 {attempt + 1}/{max_retries} 次): {str(e)}")
            if attempt < max_retries - 1:
                print("⏳ 等待 5 秒後重試...")
                import time
                time.sleep(5)
            else:
                print("⚠️ 已達到最大重試次數")
                
        except Exception as e:
            print(f"❌ 解析新聞時發生錯誤: {str(e)}")
            break
            
    return []

def generate_comic_script(topic, max_retries=3):
    print(f"📝 正在為主題生成四格漫畫腳本...")
    print(f"💭 主題：{topic}")
    
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
            print(f"🤖 正在呼叫 Google Gemini AI... (第 {attempt + 1} 次)")
            model = genai.GenerativeModel(model_name='models/gemini-2.0-flash')
            response = model.generate_content(prompt)
            
            if response.text and response.text.strip():
                print(f"✅ AI 腳本生成成功！")
                return response.text.strip()
            else:
                print(f"⚠️ AI 回應為空 (第 {attempt + 1} 次)")
                if attempt < max_retries - 1:
                    print("🔄 等待 3 秒後重試...")
                    import time
                    time.sleep(3)
                
        except Exception as e:
            print(f"❌ AI 生成失敗 (第 {attempt + 1} 次): {str(e)}")
            if attempt < max_retries - 1:
                print("🔄 等待 3 秒後重試...")
                import time
                time.sleep(3)
            else:
                print(f"⚠️ 已達到最大重試次數，跳過此主題")
                
    raise Exception("無法生成漫畫腳本")

def save_script_and_voice(topic, script, timestamp):
    import re
    print(f"💾 正在保存腳本和生成語音...")
    
    # 建立批次資料夾
    batch_dir = os.path.join(OUTPUT_DIR, timestamp)
    os.makedirs(batch_dir, exist_ok=True)
    print(f"📁 建立目錄：{batch_dir}")
    
    # 移除 Windows 不允許的檔名字元
    safe_topic = re.sub(r'[\\/:*?"<>|\s]', '_', topic)[:20]
    base = os.path.join(batch_dir, safe_topic)
    script_path = f"{base}.txt"
    voice_path = f"{base}.mp3"
    
    # 保存腳本
    print(f"📝 正在保存腳本文件...")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script)
    print(f"✅ 腳本已保存：{script_path}")
    
    # 生成語音
    print(f"🔊 正在生成中文語音（可能需要幾秒鐘）...")
    tts = gTTS(script, lang='zh-tw')
    tts.save(voice_path)
    print(f"✅ 語音已保存：{voice_path}")
    
    return script_path, voice_path

def main():
    try:
        now = datetime.now().strftime('%Y%m%d_%H%M')
        print(f"🚀 開始生成漫畫腳本 - {now}")
        print(f"{'='*50}")
        
        print(f"📰 正在從 Google News 獲取新聞...")
        topics = get_top_news(num_topics=5)
        if not topics:
            print("❌ 未找到新聞主題，程序結束")
            return
            
        print(f"✅ 成功找到 {len(topics)} 個新聞主題")
        print(f"📋 主題列表：")
        for i, topic in enumerate(topics, 1):
            print(f"   {i}. {topic}")
        print(f"{'='*50}")
        
        success_count = 0
        for idx, topic in enumerate(topics, 1):
            print(f"\n🎯 處理主題 {idx}/{len(topics)}")
            print(f"📢 主題：{topic}")
            print(f"{'-'*30}")
            
            try:
                script = generate_comic_script(topic)
                if script:
                    script_path, voice_path = save_script_and_voice(topic, script, now)
                    success_count += 1
                    print(f"✅ 主題 {idx} 處理完成！")
                else:
                    print(f"❌ 主題 {idx} 腳本生成失敗，跳過")
                
            except Exception as e:
                print(f"❌ 處理主題 '{topic}' 時發生錯誤: {str(e)}")
                continue
        
        print(f"\n{'='*50}")
        print(f"🎉 任務完成！")
        print(f"✅ 成功處理：{success_count}/{len(topics)} 個主題")
        print(f"📂 結果保存在：docs/outputs/{now}/")
        print(f"{'='*50}")
        
    except Exception as e:
        print(f"❌ 執行過程中發生錯誤: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
