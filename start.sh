#!/bin/bash
#
# AI_STICK - Main Menu
#

STICK_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$STICK_DIR"

clear
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🧠 AI_STICK MENU                          ║"
echo "║               Godman Lab Edition - Pi 5 Ready                ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  🥧 PI 5 SETUP                                               ║"
echo "║  p) 🚀 Pi 5 Setup Guide     (first-time Pi configuration)    ║"
echo "║  w) 🌐 Web Dashboard        (access from iPhone Safari)      ║"
echo "║                                                              ║"
echo "║  🤖 AI & KNOWLEDGE                                           ║"
echo "║  1) 💬 Offline AI Chat      (requires Ollama running)        ║"
echo "║  2) 📚 Start Kiwix Server   (Wikipedia/StackOverflow)        ║"
echo "║                                                              ║"
echo "║  🔄 SYNC & BACKUP                                            ║"
echo "║  3) 🔄 Smart Sync           (Mac ↔ Pi ↔ Stick)               ║"
echo "║  4) 🔄 Sync with Vertex     (backup brain & sync)            ║"
echo "║  5) 📸 Media Backup         (photos, videos, music)          ║"
echo "║                                                              ║"
echo "║  🔍 UTILITIES                                                ║"
echo "║  6) 🔍 Quick Intel          (system info gather)             ║"
echo "║  7) 🧹 Run Janitor          (pull files from Desktop)        ║"
echo "║  8) 👤 Shadow Janitor       (silent background backup)       ║"
echo "║  9) 📱 Phone Drop           (auto-pull from phone)           ║"
echo "║                                                              ║"
echo "║  📥 SETUP                                                    ║"
echo "║  d) 📥 Download Essentials  (Whisper, models)                ║"
echo "║  i) 📖 iPhone Quick Start   (SSH from Terminus)              ║"
echo "║                                                              ║"
echo "║  0) ❌ Exit                                                  ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Show stick status
USED=$(df -h "$STICK_DIR" | tail -1 | awk '{print $3}')
FREE=$(df -h "$STICK_DIR" | tail -1 | awk '{print $4}')
echo "💾 Storage: ${USED} used / ${FREE} free"
echo ""

read -p "Select option: " choice

case $choice in
    p|P)
        echo "Opening Pi 5 Setup Guide..."
        if command -v less &> /dev/null; then
            less PI5_SETUP_GUIDE.md
        else
            cat PI5_SETUP_GUIDE.md
        fi
        ;;
    w|W)
        echo "Starting Web Dashboard..."
        echo "Access from iPhone Safari: http://[YOUR_TAILSCALE_IP]:5000"
        python3 scripts/web_dashboard.py
        ;;
    1)
        echo "Starting Offline AI..."
        python3 scripts/offline_ai.py
        ;;
    2)
        echo "Opening Kiwix..."
        if [ -d "_portable_tools/kiwix/Kiwix.app" ]; then
            open "_portable_tools/kiwix/Kiwix.app"
        elif [ -f "_portable_tools/kiwix.dmg" ]; then
            echo "Mount kiwix.dmg and copy Kiwix.app to _portable_tools/kiwix/"
            open "_portable_tools/kiwix.dmg"
        else
            echo "Kiwix not installed yet. Run option 'd' first."
        fi
        ;;
    3)
        echo "Running Smart Sync..."
        python3 scripts/smart_sync.py
        ;;
    4)
        echo "Syncing with Vertex..."
        python3 scripts/vertex_sync.py
        ;;
    5)
        echo "Starting Media Backup..."
        python3 scripts/media_backup.py
        ;;
    6)
        echo "Running Quick Intel..."
        python3 scripts/quick_intel.py
        ;;
    7)
        echo "Running Janitor..."
        python3 janitor.py
        ;;
    8)
        echo "Launching Shadow Janitor in background..."
        python3 shadow_janitor.py &
        echo "Shadow Janitor is running. Check _transfer_zone for results."
        ;;
    9)
        echo "Starting Phone Drop Siphon..."
        python3 phone_drop.py
        ;;
    d|D)
        echo "Downloading essentials..."
        ./download_essentials.sh
        ;;
    i|I)
        echo "Opening iPhone Quick Start Guide..."
        if command -v less &> /dev/null; then
            less IPHONE_QUICK_START.md
        else
            cat IPHONE_QUICK_START.md
        fi
        ;;
    0)
        echo "👋 Bye!"
        exit 0
        ;;
    *)
        echo "Invalid option"
        ;;
esac

echo ""
read -p "Press Enter to return to menu..." 
exec "$0"
