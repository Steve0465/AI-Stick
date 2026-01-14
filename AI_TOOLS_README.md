# AI Tools for AI_STICK

Portable AI tools that run on your Raspberry Pi 5 with Ollama.

## 🚀 Quick Start

### Prerequisites
- Raspberry Pi 5 with Ollama installed
- AI models downloaded (mistral, phi3:mini, tinyllama)
- Python 3 with requests library (`pip3 install requests` or `apt install python3-requests`)

### Tools Overview

```
quick_ai.py        - Fast AI chat (2-3 sentence answers)
code_writer.py     - AI code generation tool
ai_agent.py        - Analyze specific files/folders
index_knowledge.py - Build searchable knowledge base
smart_ai.py        - AI with full knowledge base access
```

---

## 📱 Tool Usage

### 1. Quick AI Chat (`quick_ai.py`)

Simple questions, brief answers.

```bash
./quick_ai.py "what is Docker?"
./quick_ai.py "explain quantum computing"
./quick_ai.py "what does chmod 755 do?"
```

**Best for:** Quick facts, definitions, simple explanations

---

### 2. AI Code Writer (`code_writer.py`)

Generate code from natural language descriptions.

```bash
./code_writer.py "Python script that monitors disk space"
./code_writer.py "bash script to backup a directory"
./code_writer.py "Flask API that lists files"
```

**Features:**
- Generates production-ready code
- Adds error handling and comments
- Offers to save and make executable
- Works with any programming language

**Example:**
```bash
$ ./code_writer.py "Python script that finds large files"

🤖 Asking Mistral to write code...

📝 Generated code:
============================================================
#!/usr/bin/env python3
import os
import sys

def find_large_files(directory, min_size_mb=100):
    """Find files larger than specified size"""
    ...
============================================================

💾 Save as (or press Enter to skip): find_large.py
✅ Saved to find_large.py
✅ Made executable: chmod +x find_large.py
🚀 Run with: ./find_large.py
```

---

### 3. AI File Agent (`ai_agent.py`)

Analyze specific files or directories.

```bash
# Analyze a file
./ai_agent.py --file setup_pi5.sh "what does this script do?"
./ai_agent.py --file janitor.py "explain this code"
./ai_agent.py --file config.json "what are these settings?"

# Analyze a directory
./ai_agent.py --dir exploits "what tools are here?"
./ai_agent.py --dir wordlists "summarize these wordlists"

# General questions
./ai_agent.py "what programming languages can you help with?"
```

**Best for:** Understanding existing code, file analysis, code reviews

---

### 4. Knowledge Base System

Two-step process: Index first, then query with AI.

#### Step 1: Build Index (`index_knowledge.py`)

```bash
./index_knowledge.py
```

This scans your entire AI_STICK and creates a searchable index:
- All files and folders
- Content of text files (Python, bash, markdown, etc.)
- File sizes and locations

```
🔍 Indexing /media/pi/AI_STICK...
✅ Index saved: /tmp/ai_stick_index.json

📊 Index Summary:
   Total files: 1,247
   Total folders: 32
   Searchable text files: 156
   Total size: 15.3 GB
```

**Run this:**
- After adding new files
- When you want updated knowledge base
- Takes 10-30 seconds depending on size

---

#### Step 2: Smart AI Query (`smart_ai.py`)

Ask questions and AI automatically searches your knowledge base.

```bash
./smart_ai.py "what exploit tools do I have?"
./smart_ai.py "what Python scripts are on this stick?"
./smart_ai.py "what's in my docker folder?"
./smart_ai.py "tell me about the wordlists"
./smart_ai.py "do I have any Metasploit modules?"
```

**How it works:**
1. Extracts keywords from your question
2. Searches indexed files/folders/content
3. Builds context for AI
4. AI answers using your knowledge base

**Example:**
```bash
$ ./smart_ai.py "what exploit tools do I have?"

🧠 Using knowledge base context...

Based on your AI_STICK, you have several categories of exploit tools:

1. **Exploits folder** - Contains Metasploit modules, custom exploits, 
   and proof-of-concept code for various vulnerabilities

2. **OSINT folder** - Open source intelligence gathering tools including
   social media scrapers and metadata extracters

3. **Wordlists** - Password lists and dictionaries for security testing

[... detailed answer based on your actual files ...]
```

---

## 🎯 Workflow Examples

### Example 1: Understanding Your Code

```bash
# See what's on your stick
./smart_ai.py "what's on my AI stick?"

# Analyze specific script
./ai_agent.py --file janitor.py "what does this do?"

# Ask for improvements
./ai_agent.py --file janitor.py "how can I make this faster?"
```

### Example 2: Building New Tools

```bash
# Generate new code
./code_writer.py "Python script that organizes files by type"

# Save it as organize.py, then test
./organize.py

# Improve it
./ai_agent.py --file organize.py "add logging to this script"
```

### Example 3: Knowledge Base Queries

```bash
# Index everything
./index_knowledge.py

# Query your tools
./smart_ai.py "what tools do I have for wifi testing?"
./smart_ai.py "show me all Python scripts"
./smart_ai.py "what's in the docker folder?"
```

---

## 🧠 AI Models Guide

### Which model to use?

| Model | Speed | Quality | Best For | Size |
|-------|-------|---------|----------|------|
| **tinyllama** | ⚡⚡⚡ Fast (2-3s) | ⭐⭐ Basic | Quick facts, simple questions | 637MB |
| **phi3:mini** | ⚡⚡ Medium (5-10s) | ⭐⭐⭐⭐ Very Good | Explanations, reasoning, writing | 2.2GB |
| **mistral** | ⚡ Slower (10-20s) | ⭐⭐⭐⭐⭐ Excellent | Code generation, complex tasks | 4.1GB |

### Changing models

Edit any script and change the model parameter:

```python
"model": "mistral"      # For code and complex tasks
"model": "phi3:mini"    # For explanations
"model": "tinyllama"    # For quick answers
```

Or modify scripts to accept model as argument.

---

## 📱 iPhone Access

### Via Terminus App

1. Connect to Pi: `ssh pi@aiserver.local`
2. Navigate: `cd /media/pi/AI_STICK`
3. Run tools: `./quick_ai.py "your question"`

### Via Tailscale (Remote)

```bash
ssh pi@100.100.32.58
cd /media/pi/AI_STICK
./smart_ai.py "what tools do I have?"
```

---

## 🔧 Troubleshooting

### "Cannot connect to Ollama"
```bash
# Check if Ollama is running
systemctl status ollama

# Start it if needed
sudo systemctl start ollama

# Check models
ollama list
```

### "No such file or directory"
```bash
# Make sure you're in AI_STICK
cd /media/pi/AI_STICK

# Check if scripts exist
ls -la *.py

# Make executable
chmod +x *.py
```

### "No module named 'requests'"
```bash
# Install via apt (Debian 13)
sudo apt install python3-requests python3-tqdm

# Or use pip (if allowed)
pip3 install requests
```

### Slow responses
- Use tinyllama for faster answers
- Reduce prompt complexity
- Check Pi CPU/RAM: `htop`

---

## 💡 Tips & Tricks

### 1. Combine tools

```bash
# Generate code, then analyze it
./code_writer.py "backup script"
./ai_agent.py --file backup.sh "is this script safe?"
```

### 2. Use shorter prompts for speed

```bash
# Slow
./quick_ai.py "Can you please explain to me in detail what Docker is?"

# Fast
./quick_ai.py "what is Docker?"
```

### 3. Index regularly

```bash
# Add to cron to auto-index daily
./index_knowledge.py
```

### 4. Press Ctrl+C to stop

If AI talks too much, press Ctrl+C to stop generation.

---

## 🚀 Advanced Usage

### Batch queries

```bash
# Create query script
cat > queries.txt << EOF
what exploit tools do I have?
what Python scripts exist?
what's in docker folder?
EOF

# Run them
while read q; do
    echo "Q: $q"
    ./smart_ai.py "$q"
    echo "---"
done < queries.txt
```

### API access

All tools use Ollama's API at `http://localhost:11434`

```bash
# Test API directly
curl http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "Hello",
  "stream": false
}'
```

### Add more models

```bash
# On Pi
ollama pull llama3.2      # Meta's latest
ollama pull codellama     # Code specialist
ollama pull mistral-nemo  # Larger Mistral
```

---

## 📚 Documentation

- [Ollama API Docs](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Pi 5 Setup Guide](PI5_SETUP_GUIDE.md)
- [iPhone Quick Start](IPHONE_QUICK_START.md)

---

## 🤝 Contributing

Built with Claude Code by @memphis465

Feel free to:
- Improve the tools
- Add new features
- Create aliases and shortcuts
- Share your workflows

---

## ⚡ Quick Reference

```bash
# Chat
./quick_ai.py "question"

# Code
./code_writer.py "description"

# Analyze file
./ai_agent.py --file path "question"

# Analyze folder
./ai_agent.py --dir path "question"

# Index knowledge
./index_knowledge.py

# Smart query
./smart_ai.py "question"

# Stop generation
Ctrl+C
```

---

**Your AI. Your hardware. Zero monthly cost.** 🔥
