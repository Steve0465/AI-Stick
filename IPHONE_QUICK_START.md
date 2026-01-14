# 📱 iPhone Quick Start Guide
## Access your AI Server from anywhere

---

## STEP 1: Connect via Terminus

**After Pi setup is complete:**

1. Open **Terminus** app on iPhone
2. Tap **+** to add new host
3. Enter:
   - **Name:** AI Server
   - **Host:** Your Pi's Tailscale IP (e.g., `100.x.x.x`)
   - **Port:** `22`
   - **Username:** `pi`
   - **Password:** (your Pi password)
4. Tap **Save**
5. Tap to connect

---

## STEP 2: Quick Commands

Once connected via SSH in Terminus:

### Check Status
```bash
status
```
Shows all services, IPs, storage

### Chat with AI
```bash
aichat
```
Starts interactive chat with phi3:mini

### One-off AI Question
```bash
ollama run phi3:mini "Explain quantum computing simply"
```

### List Available Models
```bash
ollama list
```

### Ask Specific Model
```bash
ollama run tinyllama "Write a haiku about coding"
```

---

## STEP 3: Access Wikipedia (Safari)

1. Open **Safari** on iPhone
2. Go to: `http://[TAILSCALE_IP]:8080`
   - Replace `[TAILSCALE_IP]` with your Pi's IP (e.g., `100.68.45.123`)
3. Browse 119GB of Wikipedia offline!

---

## FAVORITE COMMANDS

### AI & Knowledge

```bash
# Quick AI answer
ollama run phi3:mini "Your question here"

# Start chat session
aichat

# Check what models are installed
ollama list

# Pull a new model
ollama pull qwen2.5:3b
```

### System Management

```bash
# Full status check
status

# Check disk usage
df -h /media/ai_stick

# See what's on the stick
ls -lh /media/ai_stick

# View knowledge bases
du -sh /media/ai_stick/knowledge/*
```

### Intelligence Gathering

```bash
# Run system intel gather
python3 /media/ai_stick/scripts/quick_intel.py

# Check results
ls -lh /media/ai_stick/results/intel/
```

### File Operations

```bash
# Go to stick
cd /media/ai_stick

# List recent transfers
ls -lht /media/ai_stick/_transfer_zone/ | head

# Check exports
ls -lh /media/ai_stick/Exports/
```

---

## WEB DASHBOARD ACCESS

Point Safari to: `http://[TAILSCALE_IP]:5000`

This gives you a web interface for:
- AI chat
- System status
- File browser
- Knowledge search

---

## ADVANCED: Screen/Tmux Sessions

Keep processes running even when disconnected:

### Using Tmux (recommended)

```bash
# Start new session
tmux new -s ai

# Run something (like aichat)
aichat

# Detach: Ctrl+B then D

# Reconnect later
tmux attach -t ai
```

### Run in Background

```bash
# Start process in background
python3 /media/ai_stick/shadow_janitor.py &

# See running background jobs
jobs

# Kill background job
kill %1
```

---

## TROUBLESHOOTING

### Can't Connect via Terminus

1. Check Tailscale is running on **both** devices:
   - iPhone: Open Tailscale app
   - Pi: SSH from Mac, run `tailscale status`

2. Verify IP address:
   ```bash
   # On Pi via Mac SSH
   tailscale ip -4
   ```

3. Try from Mac first:
   ```bash
   ssh pi@[TAILSCALE_IP]
   ```

### Ollama Not Responding

```bash
# Restart service
sudo systemctl restart ollama

# Check logs
sudo journalctl -u ollama -n 50
```

### Kiwix Not Loading

```bash
# Restart Kiwix
sudo systemctl restart kiwix

# Check if running
sudo systemctl status kiwix
```

### AI_STICK Not Mounted

```bash
# Check if mounted
mountpoint /media/ai_stick

# Mount manually
sudo mount -a

# Check all drives
lsblk
```

---

## SHORTCUTS WORKFLOW

### Morning Routine

1. Open Terminus
2. Connect to AI Server
3. Run `status` to check everything
4. Ask AI a question with `ollama run phi3:mini "question"`

### Research Session

1. SSH via Terminus
2. Open Safari to `http://[IP]:8080` for Wikipedia
3. Search Wikipedia for topic
4. Ask AI for clarification: `ollama run phi3:mini "explain [topic]"`

### File Transfer

1. SSH via Terminus
2. Run Shadow Janitor: `python3 /media/ai_stick/shadow_janitor.py &`
3. Let it pull files from Desktop/Downloads
4. Check results: `ls /media/ai_stick/_transfer_zone/`

---

## PRO TIPS

### 1. Use Shortcuts App

Create iOS Shortcut:
- **Trigger:** "Ask AI"
- **Action:** SSH to Pi, run command
- **Return:** Result

### 2. Siri Shortcuts

You can trigger Terminus connections via Siri Shortcuts for voice-activated SSH.

### 3. Working Copy + iSH

For advanced users:
- Use iSH app for local shell on iPhone
- Run scripts that SSH into Pi
- Automate workflows

### 4. Save Favorite Commands

In Terminus, save snippets:
- `status`
- `aichat`
- `ollama run phi3:mini ""`

Tap to run instantly.

---

## WHAT MAKES THIS POWERFUL

- **No Internet Needed:** AI runs on Pi, knowledge on USB
- **Encrypted:** Tailscale VPN encrypts all traffic
- **Private:** Everything on your hardware
- **Fast:** Local inference, no API calls
- **Portable:** Pi + USB stick + power bank
- **Access Anywhere:** As long as Pi has internet, you can reach it

You're literally SSH'd into your own AI server from your pocket.
