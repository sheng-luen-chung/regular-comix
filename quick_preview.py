# -*- coding: utf-8 -*-
import os
import sys

# Force UTF-8 encoding
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def main():
    print("=" * 50)
    print("  Regular Comix - Quick Preview")
    print("=" * 50)
    
    outputs_dir = "docs/outputs"
    if not os.path.exists(outputs_dir):
        print("No results found. Please run: python main.py")
        return
    
    # Get latest batch
    batches = [d for d in os.listdir(outputs_dir) 
              if os.path.isdir(os.path.join(outputs_dir, d))]
    
    if not batches:
        print("No batch directories found.")
        return
    
    latest = max(batches)
    print(f"Latest batch: {latest}")
    
    batch_path = os.path.join(outputs_dir, latest)
    txt_files = [f for f in os.listdir(batch_path) if f.endswith('.txt')]
    
    print(f"Found {len(txt_files)} scripts")
    print("-" * 50)
    
    for i, txt_file in enumerate(txt_files[:2], 1):
        print(f"\nScript {i}: {txt_file[:-4]}")
        print("-" * 30)
        
        try:
            with open(os.path.join(batch_path, txt_file), 'r', encoding='utf-8') as f:
                content = f.read()[:200] + "..."
                print(content)
        except Exception as e:
            print(f"Error reading file: {e}")
    
    print("\n" + "=" * 50)
    print("To view all results:")
    print("1. Run: start_web.bat")
    print("2. Open: http://127.0.0.1:5000")
    print("=" * 50)

if __name__ == "__main__":
    main()
    input("\nPress Enter to continue...")
