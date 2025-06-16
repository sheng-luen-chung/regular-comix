from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'outputs')

def get_batches():
    # 取得所有批次資料夾（依時間排序）
    batches = sorted(os.listdir(OUTPUTS_DIR), reverse=True)
    return batches

def get_scripts(batch):
    batch_dir = os.path.join(OUTPUTS_DIR, batch)
    scripts = []
    for fname in sorted(os.listdir(batch_dir)):
        if fname.endswith('.txt'):
            topic = fname[:-4]
            with open(os.path.join(batch_dir, fname), encoding='utf-8') as f:
                text = f.read()
            mp3 = topic + '.mp3'
            scripts.append({
                'topic': topic,
                'text': text,
                'mp3': mp3
            })
    return scripts

@app.route('/')
def index():
    batches = get_batches()
    latest = batches[0] if batches else None
    scripts = get_scripts(latest) if latest else []
    return render_template('index.html', batches=batches, current_batch=latest, scripts=scripts)

@app.route('/batch/<batch>')
def batch(batch):
    batches = get_batches()
    scripts = get_scripts(batch)
    return render_template('index.html', batches=batches, current_batch=batch, scripts=scripts)

@app.route('/outputs/<batch>/<filename>')
def download_file(batch, filename):
    return send_from_directory(os.path.join(OUTPUTS_DIR, batch), filename)

if __name__ == '__main__':
    print("Flask app starting...")  # 測試用
    app.run(debug=True)
    