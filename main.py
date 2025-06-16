import os
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

OUTPUT_DIR = 'outputs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_top_news(num_topics=5):
    url = 'https://news.google.com/rss?hl=zh-TW&gl=TW&ceid=TW:zh-TW'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    items = soup.find_all('item')
    topics = []
    seen = set()
    for item in items:
        title = item.title.text.strip()
        # 以標題的主題詞去重
        topic = title.split('：')[-1] if '：' in title else title
        if topic not in seen:
            seen.add(topic)
            topics.append(topic)
        if len(topics) >= num_topics:
            break
    return topics

def generate_comic_script(topic):
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
    model = genai.GenerativeModel(model_name='models/gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text.strip()

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
    now = datetime.now().strftime('%Y%m%d_%H%M')
    topics = get_top_news(num_topics=5)
    for idx, topic in enumerate(topics, 1):
        print(f"\n主題 {idx}: {topic}")
        script = generate_comic_script(topic)
        print(f"漫畫腳本：\n{script}\n")
        script_path, voice_path = save_script_and_voice(topic, script, now)
        print(f"已儲存：{script_path} 和 {voice_path}")

if __name__ == '__main__':
    main()
