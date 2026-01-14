#!/usr/bin/env python3
"""
Interactive Coding Agent with Mistral
Talk to Mistral, iterate on code, execute and test
"""
import requests
import sys
import os
import subprocess
import json

class CodingAgent:
    def __init__(self):
        self.conversation_history = []
        self.current_code = None
        self.current_filename = None

    def chat(self, message, show_code_only=False):
        """Send message to Mistral and get response"""
        # Build context from conversation history
        context = "\n".join([
            f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
            for msg in self.conversation_history[-10:]  # Last 10 messages for context
        ])

        full_prompt = f"""You are an expert coding assistant. You write clean, production-ready code with error handling and comments.

Previous conversation:
{context}

Current request: {message}

Respond naturally. If asked to write code, provide the complete code. If asked to explain, provide clear explanations."""

        try:
            response = requests.post('http://localhost:11434/api/generate',
                json={
                    "model": "mistral",
                    "prompt": full_prompt,
                    "stream": False
                },
                timeout=120)

            answer = response.json()['response']

            # Store in conversation history
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": answer})

            return answer

        except requests.exceptions.ConnectionError:
            return "❌ Cannot connect to Ollama. Is it running?\n   Run: sudo systemctl status ollama"
        except Exception as e:
            return f"❌ Error: {e}"

    def extract_code(self, text):
        """Extract code blocks from response"""
        # Look for code blocks
        import re

        # Try ```language blocks
        code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', text, re.DOTALL)
        if code_blocks:
            return code_blocks[0].strip()

        # Try to find Python/bash code patterns
        lines = text.split('\n')
        code_lines = []
        in_code = False

        for line in lines:
            # Detect code starts
            if line.strip().startswith(('#!/', 'import ', 'from ', 'def ', 'class ', 'if __name__')):
                in_code = True

            if in_code:
                code_lines.append(line)

        if code_lines:
            return '\n'.join(code_lines).strip()

        return None

    def save_code(self, code, filename=None):
        """Save code to file"""
        if not filename:
            filename = input("\n💾 Save as (or press Enter to skip): ").strip()
            if not filename:
                return None

        with open(filename, 'w') as f:
            f.write(code)

        # Make executable if script
        if filename.endswith(('.py', '.sh', '.rb', '.pl')):
            os.chmod(filename, 0o755)
            print(f"✅ Saved and made executable: {filename}")
        else:
            print(f"✅ Saved: {filename}")

        self.current_code = code
        self.current_filename = filename
        return filename

    def run_code(self, filename=None):
        """Execute the code"""
        if not filename:
            filename = self.current_filename

        if not filename or not os.path.exists(filename):
            print("❌ No file to run")
            return None

        print(f"\n🚀 Running {filename}...\n")
        print("=" * 60)

        try:
            if filename.endswith('.py'):
                result = subprocess.run(['python3', filename],
                                      capture_output=True,
                                      text=True,
                                      timeout=30)
            elif filename.endswith('.sh'):
                result = subprocess.run(['bash', filename],
                                      capture_output=True,
                                      text=True,
                                      timeout=30)
            else:
                print("❌ Don't know how to run this file type")
                return None

            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            print("=" * 60)
            print(f"\n✅ Exit code: {result.returncode}")

            return result

        except subprocess.TimeoutExpired:
            print("❌ Execution timed out (30s limit)")
            return None
        except Exception as e:
            print(f"❌ Error running code: {e}")
            return None

    def interactive_session(self):
        """Start interactive coding session"""
        print("""
╔═══════════════════════════════════════════════════════════╗
║          🤖 MISTRAL INTERACTIVE CODING AGENT 🤖           ║
╚═══════════════════════════════════════════════════════════╝

Commands:
  - Just type naturally to chat with Mistral
  - "save" - Save the last code response
  - "run" - Execute the last saved code
  - "show" - Show current code
  - "clear" - Clear conversation history
  - "exit" or "quit" - Exit

Examples:
  > write a Python script that lists all files in a directory
  > add error handling to that
  > now make it sort by size
  > save
  > run

Let's code! 🔥
""")

        while True:
            try:
                user_input = input("\n💬 You: ").strip()

                if not user_input:
                    continue

                # Commands
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 See you later!")
                    break

                elif user_input.lower() == 'save':
                    if not self.current_code:
                        print("❌ No code to save. Ask me to write something first!")
                        continue
                    self.save_code(self.current_code)
                    continue

                elif user_input.lower() == 'run':
                    if not self.current_filename:
                        print("❌ No file saved yet. Save code first with 'save'")
                        continue
                    self.run_code()
                    continue

                elif user_input.lower() == 'show':
                    if not self.current_code:
                        print("❌ No code yet")
                    else:
                        print("\n📝 Current code:")
                        print("=" * 60)
                        print(self.current_code)
                        print("=" * 60)
                    continue

                elif user_input.lower() == 'clear':
                    self.conversation_history = []
                    self.current_code = None
                    self.current_filename = None
                    print("✅ Conversation cleared")
                    continue

                # Chat with Mistral
                print("\n🤖 Mistral: ", end="", flush=True)
                response = self.chat(user_input)
                print(response)

                # Try to extract code
                code = self.extract_code(response)
                if code:
                    self.current_code = code
                    print("\n💡 Tip: Type 'save' to save this code, or 'run' to execute after saving")

            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Type 'exit' to quit or continue chatting.")
                continue
            except EOFError:
                print("\n👋 Goodbye!")
                break

if __name__ == "__main__":
    agent = CodingAgent()

    # Check if Ollama is accessible
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        models = response.json().get('models', [])
        model_names = [m['name'] for m in models]

        if 'mistral:latest' not in model_names and 'mistral' not in model_names:
            print("⚠️  Warning: Mistral model not found!")
            print("   Available models:", ', '.join(model_names))
            print("   Install with: ollama pull mistral")
            print()
    except:
        print("⚠️  Warning: Cannot connect to Ollama")
        print("   Make sure Ollama is running: sudo systemctl status ollama")
        print()

    agent.interactive_session()
