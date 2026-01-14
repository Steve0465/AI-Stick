# 🥧 RASPBERRY PI 5 + AI_STICK SETUP
## Turn your Pi into a portable AI server accessible from your iPhone

---

## THE VISION

Your Pi 5 + AI_STICK becomes a portable AI server that you can:
- SSH into from your iPhone 16 (via Terminus + Tailscale)
- Access your 437GB offline knowledge base (Wikipedia, StackOverflow, etc.)
- Run local AI models (Ollama)
- Use from anywhere on the planet via Tailscale VPN
- Sync with your Mac when home

---

## QUICK START (30 minutes)

### Step 1: Flash Raspberry Pi OS to SD Card

**On your Mac:**

1. Download Raspberry Pi Imager:
   ```bash
   brew install --cask raspberry-pi-imager
   # OR download from: https://www.raspberrypi.com/software/
   ```

2. Insert microSD card (32GB+ recommended)

3. Open Raspberry Pi Imager:
   - Choose: **Raspberry Pi OS (64-bit)** (Desktop or Lite)
   - Choose Storage: Your SD card
   - Click ⚙️ Settings:
     - ✅ Enable SSH (password authentication)
     - Set username: `pi`
     - Set password: `your_password`
     - ✅ Configure WiFi (your home network)
     - Set hostname: `aiserver` or whatever you want
   - Click WRITE

4. Insert SD card into Pi 5, plug in AI_STICK, boot it up

### Step 2: First Connection from Mac

```bash
# Find your Pi on the network
ping aiserver.local

# SSH in (from Mac)
ssh pi@aiserver.local
# Enter the password you set
```

### Step 3: Run the AI_STICK Setup Script

```bash
# On the Pi, mount the AI_STICK
ls /media/pi/AI_STICK

# If not mounted, find it:
lsblk
# Look for your USB drive, probably /dev/sda1

# Mount it
sudo mkdir -p /media/ai_stick
sudo mount /dev/sda1 /media/ai_stick

# Run the setup script
cd /media/ai_stick
sudo bash setup_pi5.sh
```

This script will:
- Install Tailscale
- Install Ollama
- Install Kiwix server
- Set up auto-mount for AI_STICK
- Configure services to auto-start
- Download lightweight AI models

**This takes about 15-20 minutes depending on your internet speed.**

### Step 4: Connect via Tailscale

**On Pi (should already be done by script):**
```bash
sudo tailscale up
# Copy the URL it gives you and open in browser to authenticate
```

**On iPhone:**
- Open Tailscale app
- You should see `aiserver` appear in your devices
- Note the IP address (something like 100.x.x.x)

**On Mac:**
- Open Tailscale
- You should see `aiserver` appear

### Step 5: Access from iPhone

**In Terminus app on iPhone:**

1. Add new host:
   - Name: `AI Server`
   - Host: `100.x.x.x` (the Tailscale IP)
   - Port: `22`
   - Username: `pi`
   - Password: (your password)

2. Connect and you're in!

**Quick Commands:**
```bash
# Start AI chat
/media/ai_stick/scripts/offline_ai.py

# Check status
/media/ai_stick/pi_status.sh

# Start Kiwix server (access Wikipedia)
# Then open http://100.x.x.x:8080 in Safari
kiwix-serve /media/ai_stick/knowledge/**/*.zim

# Query AI directly
curl http://localhost:11434/api/generate -d '{
  "model": "phi3:mini",
  "prompt": "Explain Docker in simple terms",
  "stream": false
}'
```

---

## WHAT YOU GET

### 🧠 Local AI Models (via Ollama)
- **phi3:mini** (2.3GB) - Fast, smart, runs great on Pi 5
- **tinyllama** (637MB) - Tiny but capable
- **qwen2.5:3b** (2GB) - Good at coding

### 📚 Offline Knowledge (437GB!)
- Wikipedia (119GB)
- StackOverflow (75GB)
- Books (206GB)
- Education (20GB)
- StackExchange (11GB)
- Medical info (806MB)

### 🛠 Tools
- Kiwix server (read ZIM files in browser)
- Ollama (local AI)
- All your Python scripts
- System intel gathering
- Media backup
- File janitor

---

## DAILY USAGE

### From iPhone (anywhere in the world):

1. Open Terminus
2. Connect to AI Server
3. Run commands:
   ```bash
   # Chat with AI
   ollama run phi3:mini

   # Search Wikipedia (then open in Safari)
   kiwix-serve-start

   # Check what's on the stick
   du -sh /media/ai_stick/*

   # Run intelligence gather
   python3 /media/ai_stick/scripts/quick_intel.py
   ```

### From Mac (on same Tailscale network):

```bash
# SSH in
ssh pi@100.x.x.x

# Or use the Tailscale name
ssh pi@aiserver
```

---

## AUTO-START SERVICES

The setup script creates systemd services that auto-start on boot:

- **ollama.service** - AI model server
- **kiwix.service** - Knowledge base server
- **ai-stick-automount.service** - Ensures USB is mounted

Check status:
```bash
sudo systemctl status ollama
sudo systemctl status kiwix
```

---

## UPGRADE YOUR PI SETUP

### Add More Models
```bash
# Vision model (read images)
ollama pull llava:7b

# Better coding model
ollama pull deepseek-coder:6.7b
```

### Access Kiwix from iPhone
```bash
# On Pi
kiwix-serve /media/ai_stick/knowledge/**/*.zim --port 8080

# On iPhone Safari
http://100.x.x.x:8080
```

### Set up Samba (file sharing)
```bash
sudo apt install samba
# Configure to share /media/ai_stick
# Access from Mac via Finder
```

---

## TROUBLESHOOTING

### Can't find Pi on network
```bash
# On Mac, scan network
arp -a | grep raspberry
# Or use: sudo nmap -sn 192.168.1.0/24
```

### USB not mounting
```bash
# Find the device
lsblk

# Mount manually
sudo mount /dev/sda1 /media/ai_stick
```

### Tailscale not working
```bash
# Check status
sudo tailscale status

# Reconnect
sudo tailscale up
```

### Ollama not responding
```bash
# Restart service
sudo systemctl restart ollama

# Check logs
sudo journalctl -u ollama -f
```

---

## THE COMPLETE WORKFLOW

1. **At Home:**
   - Pi 5 plugged in with AI_STICK
   - Connected to home WiFi
   - Tailscale running
   - Ollama + Kiwix auto-started

2. **From iPhone at Coffee Shop:**
   - Open Terminus
   - SSH via Tailscale (encrypted)
   - Ask AI questions
   - Search Wikipedia offline
   - All traffic encrypted via Tailscale VPN

3. **From Mac:**
   - SSH in to check status
   - Upload new models
   - Sync files
   - Update scripts

4. **On the Go:**
   - Pi 5 + AI_STICK in backpack with power bank
   - Creates its own WiFi hotspot (advanced setup)
   - iPhone connects to Pi's hotspot
   - Full AI + knowledge access anywhere

---

## ADVANCED: PORTABLE MODE

Make the Pi create its own WiFi network:

```bash
# Install hostapd
sudo apt install hostapd dnsmasq

# Configure as WiFi access point
# Then iPhone can connect directly without internet
```

This lets you use the Pi + AI_STICK completely offline in the field.

---

## WHAT MAKES THIS BADASS

- **Offline AI** - No internet needed for inference
- **437GB Knowledge** - Wikipedia, StackOverflow, books
- **Access Anywhere** - Tailscale VPN from iPhone
- **Portable** - Pi 5 + USB stick + power bank
- **Private** - All on your hardware, no cloud
- **Fast** - Pi 5 can run 7B models reasonably well

You literally have a second brain in your backpack that you can SSH into from your phone.
