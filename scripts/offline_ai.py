#!/usr/bin/env python3
"""
Offline AI Chat - Use Ollama models from the stick

Searches your offline knowledge (Wikipedia, StackOverflow) 
and uses local LLM to answer questions.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

STICK = Path("/Volumes/AI_STICK")
KNOWLEDGE = STICK / "knowledge"


def check_ollama():
    """Check if Ollama is running."""
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/tags"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            models = json.loads(result.stdout).get("models", [])
            return [m["name"] for m in models]
    except:
        pass
    return []


def ask_ollama(prompt, model="phi3:mini"):
    """Send question to Ollama."""
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/generate",
             "-d", json.dumps({"model": model, "prompt": prompt, "stream": False})],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            return json.loads(result.stdout).get("response", "No response")
    except Exception as e:
        return f"Error: {e}"
    return "Could not connect to Ollama"


def list_zim_files():
    """List available ZIM knowledge bases."""
    zims = []
    for folder in KNOWLEDGE.iterdir():
        if folder.is_dir():
            for f in folder.glob("*.zim"):
                size_gb = f.stat().st_size / (1024**3)
                zims.append({"name": f.stem, "size_gb": round(size_gb, 1), "path": str(f)})
    return zims


def main():
    print("=" * 50)
    print("🧠 OFFLINE AI - Powered by AI_STICK")
    print("=" * 50)
    
    # Check Ollama
    models = check_ollama()
    if models:
        print(f"✅ Ollama running with: {', '.join(models[:3])}")
        default_model = models[0]
    else:
        print("⚠️ Ollama not running!")
        print("   Start it with: ollama serve")
        print("   Then: ollama pull phi3:mini")
        return
    
    # Show knowledge bases
    print("\n📚 Offline Knowledge Available:")
    zims = list_zim_files()
    for z in zims[:5]:
        print(f"   • {z['name']} ({z['size_gb']}GB)")
    
    print("\n💬 Ask me anything (type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        try:
            question = input("\n🤔 You: ").strip()
            if question.lower() in ['quit', 'exit', 'q']:
                break
            if not question:
                continue
            
            print(f"\n🤖 Thinking with {default_model}...")
            
            # Enhance prompt with context
            enhanced = f"""You are a helpful assistant running offline from a USB drive.
You have access to offline Wikipedia, StackOverflow, and 60,000+ books.

Question: {question}

Provide a helpful, concise answer:"""
            
            response = ask_ollama(enhanced, default_model)
            print(f"\n🤖 AI: {response}")
            
        except KeyboardInterrupt:
            break
    
    print("\n👋 Bye!")


if __name__ == "__main__":
    main()
