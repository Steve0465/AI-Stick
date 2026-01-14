#!/usr/bin/env python3
"""
AI Agent - Analyze specific files or directories with AI
Can read files and provide context to AI for analysis
"""
import requests
import sys
import os

def read_file_context(path):
    """Read file and prepare context for AI"""
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return f"📄 File: {path}\n\n{content}\n\n---"
    except Exception as e:
        return f"❌ Could not read {path}: {e}"

def list_directory(path='.'):
    """Show AI what's in a directory"""
    try:
        files = os.listdir(path)
        context = f"📁 Directory: {path}\n\nContents ({len(files)} items):\n"
        context += "\n".join(f"  - {f}" for f in sorted(files))
        return context
    except Exception as e:
        return f"❌ Could not list {path}: {e}"

def ask_ai(question, context="", model="mistral"):
    """Ask AI with optional file context"""
    full_prompt = context + "\n\n" + question if context else question
    
    print(f"🤖 Asking {model}...\n")
    
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": model,
                "prompt": full_prompt,
                "stream": False
            },
            timeout=120)
        
        answer = response.json()['response']
        print(answer)
        return answer
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Is it running?")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("AI Agent - Analyze files and directories\n")
        print("Usage:")
        print("  ./ai_agent.py 'question'")
        print("  ./ai_agent.py --file <path> 'question about this file'")
        print("  ./ai_agent.py --dir <path> 'question about this directory'")
        print("\nExamples:")
        print("  ./ai_agent.py --file setup_pi5.sh 'explain what this does'")
        print("  ./ai_agent.py --dir exploits 'what tools are here?'")
        print("  ./ai_agent.py --file janitor.py 'add error handling to this code'")
        sys.exit(1)
    
    context = ""
    
    # Parse arguments
    if "--file" in sys.argv:
        idx = sys.argv.index("--file")
        filepath = sys.argv[idx + 1]
        context = read_file_context(filepath)
        prompt = ' '.join(sys.argv[idx + 2:])
    elif "--dir" in sys.argv or "--list" in sys.argv:
        flag = "--dir" if "--dir" in sys.argv else "--list"
        idx = sys.argv.index(flag)
        dirpath = sys.argv[idx + 1] if len(sys.argv) > idx + 1 and not sys.argv[idx + 1].startswith('-') else '.'
        # Check if next arg is the path or the question
        if len(sys.argv) > idx + 2 and not sys.argv[idx + 1].startswith('-'):
            context = list_directory(dirpath)
            prompt = ' '.join(sys.argv[idx + 2:])
        else:
            context = list_directory('.')
            prompt = ' '.join(sys.argv[idx + 1:])
    else:
        prompt = ' '.join(sys.argv[1:])
    
    ask_ai(prompt, context)
