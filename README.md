# 🧠 AI_STICK - Your Brain in a Bottle
## Portable AI Server + Knowledge Base + Hacking Lab

> **Created by Godman Lab** - Evolved through multi-agent design
> **Status:** 448GB used / 483GB free (931GB total)
> **Ready for:** Mac, Pi 5, iPhone 16 integration

---

## 🎯 THE VISION

AI_STICK is a **portable intelligence system** that gives you:

- 🧠 **Local AI Models** - Run AI completely offline (Ollama)
- 📚 **437GB Offline Knowledge** - Wikipedia, StackOverflow, 206GB of books
- 🥧 **Pi 5 Compatible** - Turn your Pi into a portable AI server
- 📱 **iPhone Accessible** - SSH from anywhere via Tailscale + Terminus
- 🔒 **Private & Encrypted** - Everything on your hardware, Tailscale VPN
- 🚀 **Bootable Kali Linux** - Full pentesting environment via Ventoy
- 🔄 **Auto-Syncing** - Smart sync between Mac, Pi, and stick

**Use Case:** Plug into your Pi 5, SSH from your iPhone 16 via Tailscale, and access your personal AI + knowledge base from anywhere on the planet.

---

## 🚀 QUICK START

### For Raspberry Pi 5 Users

1. **Flash Raspberry Pi OS** to SD card (use Raspberry Pi Imager on Mac)
2. **Plug in AI_STICK** to Pi 5
3. **SSH into Pi** from Mac: `ssh pi@aiserver.local`
4. **Run setup**: `cd /media/pi/AI_STICK && sudo bash setup_pi5.sh`
5. **Connect from iPhone**: Use Terminus app with Pi's Tailscale IP

📖 **Full Guide:** See [PI5_SETUP_GUIDE.md](PI5_SETUP_GUIDE.md)
📱 **iPhone Guide:** See [IPHONE_QUICK_START.md](IPHONE_QUICK_START.md)

### For Mac Users

1. **Plug in AI_STICK**
2. **Run menu**: `cd /Volumes/AI_STICK && ./start.sh`
3. **Choose option** from interactive menu

---

## 📁 WHAT'S INSIDE

### 🧠 AI & Knowledge (437GB)

```
knowledge/
├── wikipedia/      119GB - Full English Wikipedia
├── books/          206GB - 60,000+ ebooks
├── stackoverflow/   75GB - Stack Overflow archive
├── education/       20GB - Khan Academy, courses
├── stackexchange/   11GB - All StackExchange sites
├── guides/         4.6GB - How-to guides
├── medical/        806MB - Medical reference
└── maps/           317MB - Offline maps
```

**Access:**
- Via Kiwix server on Pi: `http://[PI_IP]:8080`
- Scripts can search and query this knowledge

### 🤖 AI Models (Coming Soon)

Optimized for Pi 5:
- **phi3:mini** (2.3GB) - Fast, efficient, smart
- **tinyllama** (637MB) - Ultra-compact
- **qwen2.5:3b** (2GB) - Coding specialist
- **llava:7b** (4.5GB) - Vision model (can read images!)

### 🔒 Security Tools

```
boot/
└── kali-live.iso   5GB - Full Kali Linux (bootable)

wordlists/          3.2GB - Password lists, SecLists
exploits/           2.4GB - Nuclei templates, payloads
osint/              76MB - OSINT tools and data
```

### 🐍 Python Scripts

```
scripts/
├── offline_ai.py         - Chat with local AI models
├── vertex_sync.py        - Sync with Vertex Brain DB
├── quick_intel.py        - Gather system intelligence
├── media_backup.py       - Backup photos/videos
├── smart_sync.py         - Mac ↔ Pi ↔ Stick sync
└── web_dashboard.py      - Web UI (access from iPhone Safari)

Root scripts:
├── janitor.py            - Pull files from Desktop/Downloads
├── shadow_janitor.py     - Silent background file collection
├── phone_drop.py         - Auto-pull from connected phones
└── start.sh              - Interactive menu system
```

---

## 💡 USAGE SCENARIOS

### Scenario 1: iPhone SSH Access (Anywhere)

1. Pi 5 at home with AI_STICK plugged in
2. Tailscale connects Pi to your iPhone
3. From coffee shop: Open Terminus → SSH to Pi
4. Ask AI questions, search Wikipedia, all offline
5. Completely encrypted via Tailscale VPN

### Scenario 2: Field Research

1. Pi 5 + AI_STICK + power bank in backpack
2. Pi creates WiFi hotspot (advanced setup)
3. iPhone connects to Pi's network
4. Access full knowledge base + AI with no internet

### Scenario 3: Mac Workflow

1. Plug AI_STICK into Mac
2. Run `./start.sh`
3. Sync files, backup data, gather intel
4. Push to Pi via Tailscale for remote access

### Scenario 4: Bootable Kali

1. Boot any PC from USB
2. Select Kali Linux in Ventoy
3. Full pentesting environment with persistence
4. All your tools and wordlists available

---

## 📱 IPHONE + TERMINUS + TAILSCALE SETUP

**The Power Combo:**
- **Tailscale** - Zero-config VPN (install on Pi, Mac, iPhone)
- **Terminus** - Professional SSH client for iOS
- **AI_STICK** - The brain that powers it all

**Setup Flow:**

1. **Pi Setup** (one-time):
   ```bash
   cd /media/pi/AI_STICK
   sudo bash setup_pi5.sh
   # Installs Ollama, Kiwix, Tailscale
   # Takes ~20 minutes
   ```

2. **iPhone Setup**:
   - Install Tailscale from App Store → Login
   - Install Terminus from App Store
   - Add host: Pi's Tailscale IP (shown after setup)

3. **Connect & Use**:
   ```bash
   # In Terminus, connect to Pi
   # Then run:
   status          # Check all services
   aichat          # Chat with AI
   ollama run phi3:mini "explain Docker"
   ```

4. **Safari Access**:
   - Open Safari: `http://[TAILSCALE_IP]:8080` → Wikipedia
   - Open Safari: `http://[TAILSCALE_IP]:5000` → Web Dashboard

---

## 🎮 INTERACTIVE MENU

Run `./start.sh` for full menu:

```
🥧 PI 5 SETUP
 p) Pi 5 Setup Guide
 w) Web Dashboard (iPhone Safari)

🤖 AI & KNOWLEDGE
 1) Offline AI Chat
 2) Start Kiwix Server

🔄 SYNC & BACKUP
 3) Smart Sync (Mac ↔ Pi ↔ Stick)
 4) Sync with Vertex
 5) Media Backup

🔍 UTILITIES
 6) Quick Intel (system info)
 7) Run Janitor (pull files)
 8) Shadow Janitor (background)
 9) Phone Drop (auto-pull)

📥 SETUP
 d) Download Essentials
 i) iPhone Quick Start
```

---

## 🔧 TECHNICAL DETAILS

### Hardware Requirements

**For Pi 5:**
- Raspberry Pi 5 (4GB+ RAM recommended)
- USB 3.0 port for AI_STICK
- MicroSD card (32GB+) for OS
- Power supply or power bank

**For Mac:**
- Any Mac with USB port
- macOS 10.15+

**For iPhone:**
- iPhone with Tailscale + Terminus apps
- iOS 15+

### Software Stack

**On Pi:**
- Raspberry Pi OS (64-bit)
- Ollama (AI model server)
- Kiwix (offline knowledge server)
- Tailscale (VPN)
- Python 3.9+

**On Mac:**
- Python 3
- Tailscale (optional)
- Standard Unix tools

### Network Architecture

```
[iPhone] ──Tailscale VPN──┐
                          ├─── [Raspberry Pi 5] ─── [AI_STICK]
[Mac]    ──Tailscale VPN──┘

All traffic encrypted end-to-end
No port forwarding needed
Works across any network
```

---

## 📊 STORAGE BREAKDOWN

```
Total:   931GB
Used:    448GB (48%)
Free:    483GB

Breakdown:
├── knowledge/       437GB ████████████████████
├── boot/           4.7GB █
├── wordlists/      3.2GB █
├── exploits/       2.4GB █
├── scripts/        768KB
└── results/        varies
```

---

## 🔐 SECURITY & ETHICS

**Important Notes:**

1. **Intel Gathering** - Only use on systems you own or have permission
2. **Shadow Janitor** - Designed for backing up YOUR files, not others
3. **Tailscale** - All traffic is encrypted and authenticated
4. **Private AI** - All inference runs on your hardware, nothing sent to cloud
5. **Kali Linux** - Use ethically for authorized pentesting only

This tool is designed for:
- Personal knowledge management
- Authorized security testing
- Offline AI research
- Educational purposes
- Privacy-focused computing

---

## 🎓 LEARNING RESOURCES

### Included Guides

- [PI5_SETUP_GUIDE.md](PI5_SETUP_GUIDE.md) - Complete Pi 5 setup
- [IPHONE_QUICK_START.md](IPHONE_QUICK_START.md) - iPhone access guide
- [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) - General setup
- [UPGRADE_SHOPPING_LIST.md](UPGRADE_SHOPPING_LIST.md) - What to add next

### External Resources

- Ollama: https://ollama.com/library
- Kiwix: https://kiwix.org
- Tailscale: https://tailscale.com/kb
- Terminus: https://termius.com

---

## 🚀 ROADMAP

### ✅ Completed
- [x] Offline knowledge base (437GB)
- [x] Pi 5 setup automation
- [x] Tailscale integration
- [x] iPhone SSH access
- [x] Web dashboard
- [x] Smart sync system
- [x] Multiple janitor scripts

### 🔄 In Progress
- [ ] Download AI models automatically
- [ ] Improve Kiwix search integration
- [ ] Add more ZIM files

### 🎯 Planned
- [ ] Pi WiFi hotspot mode (fully offline)
- [ ] Voice interface via Whisper
- [ ] Image analysis via LLaVA
- [ ] Automated backups to cloud (optional)
- [ ] Docker containers for tools
- [ ] More OSINT automation

---

## 💬 SUPPORT

**Documentation:**
- See guides in root directory
- Check scripts/ for implementation details

**Common Issues:**
- Pi not mounting stick: Check `/etc/fstab` and UUID
- Tailscale not connecting: Run `sudo tailscale up`
- Ollama not responding: `sudo systemctl restart ollama`

**Contributing:**
This is a personal project, but feel free to fork and adapt!

---

## 📜 LICENSE

Personal use only. Knowledge bases are subject to their own licenses.

---

## 🏆 CREDITS

**Created by:** Godman Lab (Stephen Godman)
**Design Evolution:** Multi-agent collaborative design
**Production Implementation:** Jean-Claude Van Damme (Claude Sonnet 4.5) - 2026-01-13

**Contributors:**
- 🥋 **Jean-Claude Van Damme** (Claude Sonnet 4.5) - Production system, Pi integration, security hardening
- 🤖 **Claude Collective** (Various) - Knowledge base, scripts, architecture
- 🐦 **Grok** (xAI) - Shadow Janitor, stealth operations
- 👤 **Stephen Godman** (Human) - Vision, curation, enablement

**Philosophy:** Privacy-first, offline-capable, truly portable intelligence

*See [CONTRIBUTORS.md](CONTRIBUTORS.md) for detailed credits*
*See [CHANGELOG.md](CHANGELOG.md) for version history*

---

## 🎉 GETTING STARTED NOW

**If you have a Pi 5:**
```bash
# 1. Flash Raspberry Pi OS to SD card
# 2. Boot Pi with AI_STICK plugged in
# 3. SSH from Mac
ssh pi@aiserver.local

# 4. Run setup
cd /media/pi/AI_STICK
sudo bash setup_pi5.sh

# 5. Connect from iPhone (Terminus app)
# Use the Tailscale IP shown after setup
```

**If you're on Mac:**
```bash
# Plug in AI_STICK
cd /Volumes/AI_STICK
./start.sh
```

**Need help?** Read the guides:
- 🥧 `PI5_SETUP_GUIDE.md` for Pi setup
- 📱 `IPHONE_QUICK_START.md` for iPhone access
- 📚 `UPGRADE_SHOPPING_LIST.md` for what to add

---

**Welcome to your portable brain. 🧠**
