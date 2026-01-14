# 🚀 AI_STICK QUICK START

**Plug into Pi → SSH in → Start coding with AI**

---

## 📱 Connect from iPhone

```bash
ssh pi@aiserver.local
# or via Tailscale:
ssh pi@100.100.32.58
```

---

## ⚡ First Time Setup

```bash
cd /media/pi/AI_STICK
./check_system.sh    # Verify everything works
```

If anything is missing:
```bash
sudo apt install python3-requests python3-tqdm
```

---

## 🤖 Interactive Coding (BEST WAY)

```bash
./coding_agent.py
```

Then just talk:
```
You: write a Python script that organizes files by type
Mistral: [writes code]

You: add error handling
Mistral: [improves it]

You: save
You: run
You: perfect!
```

**Read full guide:** `cat CODING_AGENT_GUIDE.md`

---

## 🔥 Quick Commands

```bash
# Fast questions (2-3 sentence answers)
./quick_ai.py "what is Docker?"

# Generate code (one-shot)
./code_writer.py "bash script to backup a directory"

# Analyze files
./ai_agent.py --file setup_pi5.sh "explain this"

# Search your knowledge base
./smart_ai.py "what exploit tools do I have?"

# Index your files (do this once)
./index_knowledge.py
```

---

## 📚 Documentation

- `CODING_AGENT_GUIDE.md` - Interactive coding (START HERE)
- `AI_TOOLS_README.md` - All AI tools explained
- `PI5_SETUP_GUIDE.md` - Hardware setup
- `IPHONE_QUICK_START.md` - Mobile access
- `README.md` - Full project overview

---

## 🎯 Common Tasks

### Write Code
```bash
./coding_agent.py
> write a [description]
> save
> run
```

### Ask Questions
```bash
./quick_ai.py "your question"
```

### Analyze Your Files
```bash
./smart_ai.py "what's on my AI stick?"
```

### Generate One-Off Scripts
```bash
./code_writer.py "what you need"
```

---

## 🛠️ Troubleshooting

### Ollama not responding?
```bash
sudo systemctl status ollama
sudo systemctl restart ollama
ollama list  # Check models
```

### Script not executable?
```bash
chmod +x *.py
```

### Python package missing?
```bash
sudo apt install python3-requests python3-tqdm
```

---

## 💡 Pro Tips

1. **Use the interactive agent** - It's way better than one-shot commands
2. **Index your knowledge base** - Run `./index_knowledge.py` once
3. **Test on the Pi first** - Make sure everything works before going remote
4. **Save your best scripts** - Build a personal toolkit

---

## 🔥 The Power Workflow

```bash
# 1. Start interactive coding
./coding_agent.py

# 2. Build something
You: write a system monitor
Mistral: [codes]
You: save
You: run

# 3. Query knowledge
# (open new SSH session)
./smart_ai.py "what tools do I have for networking?"

# 4. Analyze files
./ai_agent.py --dir scripts "what's in here?"
```

---

**Everything runs locally. Zero cost. 100% yours.** 🎉

Start here: `./coding_agent.py`
