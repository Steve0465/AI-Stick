#!/usr/bin/env python3
"""
Knowledge Indexer - Indexes all content on AI_STICK for AI access
Creates a searchable index of files, folders, and content
"""
import os
import json
from pathlib import Path

def should_skip(name):
    """Check if file/folder should be skipped"""
    skip_patterns = [
        '.', '._', '$RECYCLE', 'System Volume',
        '.Spotlight', '.fseventsd', '.Trashes'
    ]
    return any(pattern in name for pattern in skip_patterns)

def is_text_file(filename):
    """Check if file is a text file we can index"""
    text_extensions = [
        '.txt', '.md', '.py', '.sh', '.js', '.json', '.yaml', '.yml',
        '.conf', '.cfg', '.ini', '.xml', '.html', '.css', '.sql',
        '.go', '.rs', '.c', '.cpp', '.h', '.java', '.rb', '.pl'
    ]
    return any(filename.lower().endswith(ext) for ext in text_extensions)

def index_stick(base_path='/media/pi/AI_STICK'):
    """Index all content on AI_STICK"""
    # Handle both Pi and Mac paths
    if not os.path.exists(base_path):
        base_path = '/Volumes/AI_STICK'
    
    if not os.path.exists(base_path):
        print(f"❌ AI_STICK not found at {base_path}")
        return None
    
    print(f"🔍 Indexing {base_path}...")
    
    index = {
        'base_path': base_path,
        'files': [],
        'folders': {},
        'text_files': [],
        'stats': {
            'total_files': 0,
            'total_folders': 0,
            'text_files': 0,
            'total_size': 0
        }
    }
    
    for root, dirs, files in os.walk(base_path):
        # Filter out hidden/system folders
        dirs[:] = [d for d in dirs if not should_skip(d)]
        
        folder_name = root.replace(base_path + '/', '').replace(base_path, '')
        if folder_name and folder_name != base_path:
            index['folders'][folder_name] = []
            index['stats']['total_folders'] += 1
        
        for file in files:
            if should_skip(file):
                continue
            
            filepath = os.path.join(root, file)
            relative_path = filepath.replace(base_path + '/', '').replace(base_path + '\\', '')
            
            try:
                size = os.path.getsize(filepath)
                index['stats']['total_size'] += size
            except:
                size = 0
            
            file_info = {
                'path': relative_path,
                'name': file,
                'size': size,
                'folder': folder_name if folder_name else 'root'
            }
            
            # Index text files for content search
            if is_text_file(file):
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(10000)  # First 10KB
                    file_info['preview'] = content[:500]
                    file_info['searchable'] = True
                    index['text_files'].append(file_info)
                    index['stats']['text_files'] += 1
                except:
                    pass
            
            index['files'].append(file_info)
            index['stats']['total_files'] += 1
            
            if folder_name in index['folders']:
                index['folders'][folder_name].append(file)
    
    # Save index to both Pi and Mac compatible locations
    index_paths = [
        '/tmp/ai_stick_index.json',
        os.path.join(base_path, '.ai_index.json')
    ]
    
    for index_path in index_paths:
        try:
            with open(index_path, 'w') as f:
                json.dump(index, f, indent=2)
            print(f"✅ Index saved: {index_path}")
        except:
            pass
    
    # Print summary
    print(f"\n📊 Index Summary:")
    print(f"   Total files: {index['stats']['total_files']}")
    print(f"   Total folders: {index['stats']['total_folders']}")
    print(f"   Searchable text files: {index['stats']['text_files']}")
    print(f"   Total size: {index['stats']['total_size'] / (1024**3):.2f} GB")
    
    return index

if __name__ == "__main__":
    index = index_stick()
    if index:
        print("\n✅ Indexing complete! Use smart_ai.py to query with AI.")
