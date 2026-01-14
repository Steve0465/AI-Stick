#!/usr/bin/env python3
"""
Smart AI - AI with full knowledge base access
Automatically searches AI_STICK and provides context to Mistral
"""
import requests
import json
import sys
import os

def load_index():
    """Load the AI_STICK index"""
    index_paths = [
        '/tmp/ai_stick_index.json',
        '/Volumes/AI_STICK/.ai_index.json',
        '/media/pi/AI_STICK/.ai_index.json'
    ]
    
    for path in index_paths:
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            continue
    
    return None

def search_knowledge(query, index):
    """Search through indexed content"""
    results = {
        'files': [],
        'folders': [],
        'content': []
    }
    
    query_words = [w.lower() for w in query.split() if len(w) > 3]
    
    # Search file names
    for file_info in index['files']:
        for word in query_words:
            if word in file_info['name'].lower() or word in file_info.get('folder', '').lower():
                results['files'].append(file_info['path'])
                break
    
    # Search content in text files
    for file_info in index.get('text_files', []):
        if 'preview' in file_info:
            for word in query_words:
                if word in file_info['preview'].lower():
                    results['content'].append({
                        'file': file_info['path'],
                        'preview': file_info['preview'][:200]
                    })
                    break
    
    # Search folder names
    for folder in index['folders'].keys():
        for word in query_words:
            if word in folder.lower():
                results['folders'].append(folder)
                break
    
    return results

def build_context(question, index):
    """Build context for AI from knowledge base"""
    # Search for relevant content
    search_results = search_knowledge(question, index)
    
    context_parts = []
    
    # Add general overview
    context_parts.append(f"📚 KNOWLEDGE BASE: AI_STICK")
    context_parts.append(f"Total files: {index['stats']['total_files']}")
    context_parts.append(f"Total folders: {index['stats']['total_folders']}\n")
    
    # Add relevant folders
    if search_results['folders']:
        context_parts.append("📁 Relevant folders:")
        for folder in search_results['folders'][:5]:
            files = index['folders'].get(folder, [])
            context_parts.append(f"  - {folder}/ ({len(files)} files)")
    
    # Add relevant files
    if search_results['files']:
        context_parts.append("\n📄 Relevant files:")
        for filepath in search_results['files'][:10]:
            context_parts.append(f"  - {filepath}")
    
    # Add content matches
    if search_results['content']:
        context_parts.append("\n📝 Content matches:")
        for match in search_results['content'][:3]:
            context_parts.append(f"  File: {match['file']}")
            context_parts.append(f"  Preview: {match['preview']}...")
    
    # If no specific matches, show folder structure
    if not any([search_results['folders'], search_results['files'], search_results['content']]):
        context_parts.append("\n📂 Main folders available:")
        for folder in list(index['folders'].keys())[:15]:
            context_parts.append(f"  - {folder}/")
    
    context_parts.append("\n---\nUser question:")
    
    return "\n".join(context_parts)

def ask_with_knowledge(question):
    """Ask AI with automatic knowledge retrieval"""
    index = load_index()
    
    if not index:
        print("⚠️  No knowledge index found. Run: ./index_knowledge.py")
        print("    Falling back to basic AI without knowledge base...\n")
        context = ""
    else:
        context = build_context(question, index)
        print("🧠 Using knowledge base context...\n")
    
    try:
        response = requests.post('http://localhost:11434/api/generate',
            json={
                "model": "mistral",
                "prompt": context + "\n" + question,
                "stream": False
            },
            timeout=120)
        
        answer = response.json()['response']
        print(answer)
        return answer
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Is the Pi running?")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Smart AI - AI with full knowledge base access\n")
        print("Usage: ./smart_ai.py 'your question'")
        print("\nExamples:")
        print("  ./smart_ai.py 'what exploit tools do I have?'")
        print("  ./smart_ai.py 'what Python scripts are on this stick?'")
        print("  ./smart_ai.py 'what is in the docker folder?'")
        print("  ./smart_ai.py 'tell me about my wordlists'")
        print("\nNote: Run ./index_knowledge.py first to build the knowledge base")
        sys.exit(1)
    
    question = ' '.join(sys.argv[1:])
    ask_with_knowledge(question)
