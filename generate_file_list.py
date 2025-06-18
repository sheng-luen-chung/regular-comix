#!/usr/bin/env python3
"""
生成 file-list.json 用於 GitHub Pages 靜態載入
"""
import os
import json
from pathlib import Path

def generate_file_list():
    """生成檔案清單 JSON"""
    outputs_dir = Path('docs/outputs')
    
    if not outputs_dir.exists():
        print(f"❌ 目錄不存在: {outputs_dir}")
        return
    
    file_list = {}
    
    # 遍歷所有批次目錄
    for batch_dir in sorted(outputs_dir.iterdir(), reverse=True):
        if not batch_dir.is_dir():
            continue
            
        batch_name = batch_dir.name
        file_list[batch_name] = []
        
        print(f"📁 處理批次: {batch_name}")
        
        # 遍歷批次目錄中的檔案
        txt_files = []
        mp3_files = []
        
        for file_path in batch_dir.iterdir():
            if file_path.is_file():
                if file_path.suffix == '.txt':
                    txt_files.append(file_path.stem)
                elif file_path.suffix == '.mp3':
                    mp3_files.append(file_path.stem)
        
        # 配對 txt 和 mp3 檔案
        for txt_name in txt_files:
            has_mp3 = txt_name in mp3_files
            file_list[batch_name].append({
                'name': txt_name,
                'txt': f'{txt_name}.txt',
                'mp3': f'{txt_name}.mp3' if has_mp3 else None
            })
            
        print(f"   ✅ 找到 {len(file_list[batch_name])} 個檔案")
    
    # 寫入 JSON 檔案
    output_file = Path('docs/file-list.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(file_list, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 檔案清單已生成: {output_file}")
    print(f"📊 總共 {len(file_list)} 個批次")

if __name__ == '__main__':
    generate_file_list()
