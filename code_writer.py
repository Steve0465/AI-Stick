#!/usr/bin/env python3
"""
Code Writer - AI-powered code generation tool
Usage: ./code_writer.py 'description of code you want'
"""
import requests
import json
import sys
import os

def write_code(prompt):
    """Generate code using Mistral"""
    print(f"🤖 Asking Mistral to write code...\n")
    
    full_prompt = f"""Write production-ready, well-commented code for: {prompt}

Requirements:
- Include error handling
- Add helpful comments
- Make it readable and maintainable
- Provide ONLY the code, no explanations before or after

Code:"""
    
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "mistral",
                "prompt": full_prompt,
                "stream": False
            },
            timeout=120)
        
        code = response.json()['response']
        
        print("📝 Generated code:\n")
        print("=" * 60)
        print(code)
        print("=" * 60)
        
        # Ask for filename
        filename = input("\n💾 Save as (or press Enter to skip): ").strip()
        
        if filename:
            # Ensure it has proper extension
            if not any(filename.endswith(ext) for ext in ['.py', '.sh', '.js', '.go', '.rs']):
                print("⚠️  Warning: File has no extension. Consider adding .py, .sh, etc.")
            
            with open(filename, 'w') as f:
                f.write(code)
            print(f"✅ Saved to {filename}")
            
            # Make executable if it's a script
            if filename.endswith(('.py', '.sh', '.rb', '.pl')):
                os.chmod(filename, 0o755)
                print(f"✅ Made executable: chmod +x {filename}")
                print(f"\n🚀 Run with: ./{filename}")
        
        return code
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Is it running?")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./code_writer.py 'description of what you want to build'")
        print("\nExamples:")
        print("  ./code_writer.py 'Python script that monitors disk space'")
        print("  ./code_writer.py 'bash script that backs up a directory'")
        print("  ./code_writer.py 'Python Flask API that lists files'")
        sys.exit(1)
    
    prompt = ' '.join(sys.argv[1:])
    write_code(prompt)
