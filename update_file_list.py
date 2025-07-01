import os
import json

def generate_file_list():
    """生成 file-list.json，只包含實際存在的批次和檔案"""
    
    outputs_dir = 'docs/outputs'
    file_list = {}
    
    if not os.path.exists(outputs_dir):
        print(f"目錄不存在: {outputs_dir}")
        return
    
    # 掃描所有批次目錄
    for batch_name in os.listdir(outputs_dir):
        batch_path = os.path.join(outputs_dir, batch_name)
        
        if not os.path.isdir(batch_path):
            continue
            
        batch_files = []
        txt_files = [f for f in os.listdir(batch_path) if f.endswith('.txt')]
        
        for txt_file in txt_files:
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
            print(f"✅ 批次 {batch_name}: {len(batch_files)} 個檔案")
        else:
            print(f"⚠️  批次 {batch_name}: 沒有檔案，跳過")
    
    # 寫入 JSON 檔案
    output_file = 'docs/file-list.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(file_list, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 已生成 {output_file}")
    print(f"📊 總共包含 {len(file_list)} 個有內容的批次")

if __name__ == '__main__':
    generate_file_list()
