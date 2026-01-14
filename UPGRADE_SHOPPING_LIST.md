# 🚀 AI_STICK UPGRADE SHOPPING LIST
## You have 483GB free - let's fill it with awesome

---

## 🧠 AI MODELS TO ADD (~100GB)

### For Ollama (run on Pi or Mac)
```bash
# Small & Fast (will run on Pi 5)
ollama pull phi3:mini              # 2.3GB - Microsoft's tiny genius
ollama pull llama3.2:3b            # 2GB - Meta's small model
ollama pull qwen2.5:3b             # 2GB - Alibaba's coder
ollama pull gemma2:2b              # 1.6GB - Google's tiny model
ollama pull tinyllama              # 637MB - Smallest usable model

# Medium (Mac only - too big for Pi)
ollama pull llama3.1:8b            # 4.7GB - Sweet spot for local
ollama pull mistral:7b             # 4.1GB - Fast & capable
ollama pull codellama:7b           # 3.8GB - Coding specialist
ollama pull deepseek-coder:6.7b    # 3.8GB - Another good coder

# Uncensored (for when you need raw answers)
ollama pull dolphin-llama3:8b      # 4.7GB - No safety filters
ollama pull nous-hermes2:10.7b     # 6.1GB - Very capable uncensored

# Specialty
ollama pull llava:7b               # 4.5GB - VISION! Can see images
ollama pull bakllava               # 4.5GB - Another vision model
```

### GGUF Files (for llama.cpp / Pi)
Download from: https://huggingface.co/TheBloke
- phi-3-mini-4k-instruct.Q4_K_M.gguf (~2GB)
- TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf (~700MB)
- Mistral-7B-Instruct-v0.2.Q4_K_M.gguf (~4GB)

---

## 🎤 SPEECH MODELS (~5GB)

### Whisper (Speech-to-Text)
```bash
# For whisper.cpp on Pi
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin      # 75MB - Fast
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin      # 142MB - Better
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin     # 466MB - Good balance
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.en.bin    # 1.5GB - Great quality
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin     # 3GB - Best quality
```

### Piper (Text-to-Speech) 
Fast TTS that runs locally
```bash
# Download voices from: https://github.com/rhasspy/piper/releases
# en_US-lessac-medium.onnx - Natural sounding
# en_US-ryan-medium.onnx - Male voice
```

---

## 📚 MORE OFFLINE KNOWLEDGE (~50GB)

### ZIM Files from Kiwix (kiwix.org/download)
- **khan-academy** (~40GB) - Math, science, economics courses
- **ted** (~8GB) - TED talks
- **mdwiki** (~1GB) - Medical Wikipedia
- **wikibooks** (~2GB) - Textbooks
- **wikihow** (~15GB) - How-to guides for everything
- **ifixit** (~3GB) - Repair guides for electronics

### Other Datasets
- **Common Crawl samples** - Web scrape data
- **The Pile** (subset) - Training data mixture
- **Arxiv papers** (CS subset) - Academic papers

---

## 🔧 PORTABLE TOOLS TO ADD

### AI/ML Tools
```
_portable_tools/
├── ollama/                    # Portable Ollama
├── llama.cpp/                 # CPU inference
├── whisper.cpp/               # Speech recognition  
├── stable-diffusion.cpp/      # Image generation (needs GPU)
├── text-generation-webui/     # Nice UI for models
└── open-webui/                # ChatGPT-like interface
```

### Productivity
```
├── obsidian/                  # Note-taking (portable)
├── zotero/                    # Research management
├── calibre/                   # Ebook management
└── kiwix/                     # ZIM file reader
```

### Security/OSINT (expand what you have)
```
├── maltego/                   # OSINT visualization
├── spiderfoot/                # Automated OSINT
├── recon-ng/                  # Web recon framework
├── sherlock/                  # Username hunter
├── holehe/                    # Email OSINT
└── maigret/                   # Username search
```

---

## 🎮 BOOTABLE ISOS TO ADD (~30GB)

### For Ventoy
- **Tails** (~1.3GB) - Anonymous OS
- **Parrot Security** (~4GB) - Alternative to Kali
- **Ubuntu Server** (~2GB) - For quick server setup
- **Hiren's BootCD PE** (~3GB) - Windows rescue
- **SystemRescue** (~800MB) - Linux rescue
- **Clonezilla** (~500MB) - Disk cloning
- **GParted** (~500MB) - Partition management
- **Medicat** (~20GB) - Ultimate PC repair toolkit

---

## 🤖 CLEVER TRICKS

### 1. Auto-Detect & Load
Create `autorun.sh` that detects the host system and offers:
- "Run local AI chat"
- "Start Kiwix server"  
- "Sync with Vertex"
- "Boot to Kali"

### 2. Portable Python Environment
```bash
# Miniconda portable install
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
# Install to _portable_runtimes/miniconda
```

### 3. Emergency Vertex Backup
Script that backs up vertex_brain.db to the stick

### 4. "Phone Home" Script
When plugged into any PC:
- Pulls files matching patterns
- Encrypts and stores
- Leaves no trace

### 5. Kiwix + Ollama = Offline AI with Citations
- Query Ollama
- Search Wikipedia/StackOverflow via Kiwix API
- Return answers with sources

### 6. USB Rubber Ducky Payloads
(In a locked folder for ethical use only)
- Auto-backup scripts
- Quick system info gather
- WiFi password recovery

---

## 📥 DOWNLOAD COMMANDS

### Quick Setup Script
```bash
#!/bin/bash
# Run this to download the essentials

STICK="/Volumes/AI_STICK"
MODELS="$STICK/models/ollama"
WHISPER="$STICK/models/whisper"

mkdir -p "$MODELS" "$WHISPER"

# Whisper models
cd "$WHISPER"
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin

# Ollama will download to its own location, but you can export:
# OLLAMA_MODELS="$MODELS" ollama pull phi3:mini

echo "Done! Models saved to $STICK/models/"
```

---

## PRIORITY ORDER

1. **Whisper models** (5GB) - Voice memo transcription
2. **Small Ollama models** (10GB) - phi3, tinyllama, qwen2.5
3. **llava vision model** (4.5GB) - Read images/receipts
4. **Khan Academy ZIM** (40GB) - Education
5. **WikiHow ZIM** (15GB) - Practical guides
6. **Tails + SystemRescue ISOs** (5GB) - Emergency tools

**Total Priority Items: ~80GB**
**Remaining after: ~400GB**

---

## THE VISION

```
AI_STICK becomes your "brain in a bottle":

1. Plug into ANY computer
2. Boot to Kali OR run portable tools
3. Full Wikipedia + StackOverflow searchable offline
4. Local AI that can:
   - Answer questions (Ollama)
   - Transcribe voice (Whisper)
   - Read images (LLaVA)
   - Generate code
5. Syncs with Vertex when home
6. Works on planes, in the field, anywhere
```

You literally carry your second brain in your pocket.
