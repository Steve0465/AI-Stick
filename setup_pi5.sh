#!/bin/bash
#
# AI_STICK Pi 5 Setup Script
# Run this on your Pi 5 to set up everything automatically
#

set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║     🥧 RASPBERRY PI 5 + AI_STICK SETUP                ║"
echo "║     Transforming your Pi into a portable AI server    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if running on Pi
if [ ! -f /proc/device-tree/model ] || ! grep -q "Raspberry Pi" /proc/device-tree/model; then
    echo "⚠️  Warning: This doesn't look like a Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Determine AI_STICK location
if [ -d "/media/pi/AI_STICK" ]; then
    STICK="/media/pi/AI_STICK"
elif [ -d "/media/ai_stick" ]; then
    STICK="/media/ai_stick"
else
    echo "❌ Cannot find AI_STICK mount point"
    echo "Please mount the USB drive first:"
    echo "  sudo mkdir -p /media/ai_stick"
    echo "  sudo mount /dev/sda1 /media/ai_stick"
    exit 1
fi

echo "✅ Found AI_STICK at: $STICK"
echo ""

# Update system
echo "📦 Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install essentials
echo "📦 Installing essential packages..."
sudo apt install -y \
    curl \
    git \
    python3-pip \
    python3-venv \
    htop \
    tmux \
    vim \
    jq \
    wget \
    build-essential \
    cmake

echo ""
echo "══════════════════════════════════════════════════════"
echo "🔗 INSTALLING TAILSCALE"
echo "══════════════════════════════════════════════════════"

# Install Tailscale
if ! command -v tailscale &> /dev/null; then
    curl -fsSL https://tailscale.com/install.sh | sh
    echo "✅ Tailscale installed"

    echo ""
    echo "🔑 Starting Tailscale setup..."
    echo "You'll need to authenticate in a browser."
    echo "The command will give you a URL to visit."
    echo ""
    sudo tailscale up

    echo ""
    echo "✅ Tailscale connected!"
    echo "Your Tailscale IP: $(tailscale ip -4)"
else
    echo "✅ Tailscale already installed"
    echo "Your Tailscale IP: $(tailscale ip -4)"
fi

echo ""
echo "══════════════════════════════════════════════════════"
echo "🧠 INSTALLING OLLAMA (AI Models)"
echo "══════════════════════════════════════════════════════"

# Install Ollama
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
    echo "✅ Ollama installed"
else
    echo "✅ Ollama already installed"
fi

# Start Ollama service
sudo systemctl enable ollama
sudo systemctl start ollama

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama to start..."
sleep 5

# Download lightweight models for Pi
echo ""
echo "📥 Downloading AI models optimized for Pi 5..."
echo "This will take 10-15 minutes depending on your connection."
echo ""

# phi3:mini - Best balance for Pi 5
if ! ollama list | grep -q "phi3:mini"; then
    echo "Downloading phi3:mini (2.3GB) - Microsoft's efficient model..."
    ollama pull phi3:mini
fi

# tinyllama - Smallest usable model
if ! ollama list | grep -q "tinyllama"; then
    echo "Downloading tinyllama (637MB) - Ultra compact model..."
    ollama pull tinyllama
fi

echo "✅ AI models installed!"
ollama list

echo ""
echo "══════════════════════════════════════════════════════"
echo "📚 INSTALLING KIWIX (OFFLINE KNOWLEDGE SERVER)"
echo "══════════════════════════════════════════════════════"

# Install Kiwix
if ! command -v kiwix-serve &> /dev/null; then
    sudo apt install -y kiwix-tools
    echo "✅ Kiwix installed"
else
    echo "✅ Kiwix already installed"
fi

# Create Kiwix startup script
echo "Creating Kiwix startup script..."

sudo tee /usr/local/bin/start-kiwix.sh > /dev/null <<'EOFKIWIX'
#!/bin/bash
# Find all ZIM files and serve them
ZIM_FILES=$(find /media/ai_stick/knowledge -name "*.zim" -type f 2>/dev/null)
if [ -n "$ZIM_FILES" ]; then
    exec /usr/bin/kiwix-serve --port=8080 $ZIM_FILES
else
    echo "No ZIM files found in /media/ai_stick/knowledge"
    exit 1
fi
EOFKIWIX

sudo chmod +x /usr/local/bin/start-kiwix.sh

# Create Kiwix systemd service
echo "Creating Kiwix auto-start service..."

sudo tee /etc/systemd/system/kiwix.service > /dev/null <<'EOFSERVICE'
[Unit]
Description=Kiwix Server - Offline Knowledge Base
After=network.target

[Service]
Type=simple
User=pi
ExecStart=/usr/local/bin/start-kiwix.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOFSERVICE

sudo systemctl daemon-reload
sudo systemctl enable kiwix
sudo systemctl start kiwix

echo "✅ Kiwix server running on port 8080"

echo ""
echo "══════════════════════════════════════════════════════"
echo "🔧 CONFIGURING AUTO-MOUNT FOR AI_STICK"
echo "══════════════════════════════════════════════════════"

# Get USB device UUID
USB_DEVICE=$(findmnt -n -o SOURCE "$STICK" | head -1)
USB_UUID=$(sudo blkid -s UUID -o value $USB_DEVICE)

echo "USB Device: $USB_DEVICE"
echo "UUID: $USB_UUID"

# Add to fstab if not already there
if ! grep -q "$USB_UUID" /etc/fstab; then
    echo "Adding to /etc/fstab for auto-mount..."
    echo "UUID=$USB_UUID /media/ai_stick exfat defaults,nofail,x-systemd.device-timeout=5 0 0" | sudo tee -a /etc/fstab
    echo "✅ Auto-mount configured"
else
    echo "✅ Already in fstab"
fi

# Create mount point
sudo mkdir -p /media/ai_stick

# Create symlink for convenience
ln -sf /media/ai_stick ~/ai_stick 2>/dev/null || true

echo ""
echo "══════════════════════════════════════════════════════"
echo "🐍 SETTING UP PYTHON ENVIRONMENT"
echo "══════════════════════════════════════════════════════"

# Install Python packages
pip3 install --user requests

echo ""
echo "══════════════════════════════════════════════════════"
echo "🚀 CREATING HELPER SCRIPTS"
echo "══════════════════════════════════════════════════════"

# Create status check script
cat > ~/pi_status.sh <<'EOFSTATUS'
#!/bin/bash
echo "╔════════════════════════════════════════════════════════╗"
echo "║              🥧 AI SERVER STATUS                       ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Tailscale
if command -v tailscale &> /dev/null; then
    TS_IP=$(tailscale ip -4 2>/dev/null)
    if [ -n "$TS_IP" ]; then
        echo "🔗 Tailscale: ✅ Connected - $TS_IP"
    else
        echo "🔗 Tailscale: ❌ Not connected"
    fi
else
    echo "🔗 Tailscale: ❌ Not installed"
fi

# Ollama
if systemctl is-active --quiet ollama; then
    echo "🧠 Ollama: ✅ Running"
    MODELS=$(ollama list 2>/dev/null | tail -n +2 | wc -l)
    echo "   Models: $MODELS installed"
else
    echo "🧠 Ollama: ❌ Not running"
fi

# Kiwix
if systemctl is-active --quiet kiwix; then
    echo "📚 Kiwix: ✅ Running on http://localhost:8080"
else
    echo "📚 Kiwix: ❌ Not running"
fi

# AI_STICK
if mountpoint -q /media/ai_stick; then
    USED=$(df -h /media/ai_stick | tail -1 | awk '{print $3}')
    FREE=$(df -h /media/ai_stick | tail -1 | awk '{print $4}')
    echo "💾 AI_STICK: ✅ Mounted - ${USED} used / ${FREE} free"
else
    echo "💾 AI_STICK: ❌ Not mounted"
fi

# System info
echo ""
echo "📊 System:"
echo "   CPU Temp: $(vcgencmd measure_temp | cut -d= -f2)"
echo "   Memory: $(free -h | awk 'NR==2{print $3 "/" $2}')"
echo "   Uptime: $(uptime -p)"
echo ""
EOFSTATUS

chmod +x ~/pi_status.sh

# Create quick AI chat launcher
cat > ~/ai_chat.sh <<'EOFCHAT'
#!/bin/bash
echo "🧠 Starting AI Chat (Ctrl+D to exit)"
echo "Using model: phi3:mini"
echo ""
ollama run phi3:mini
EOFCHAT

chmod +x ~/ai_chat.sh

# Add helpful aliases to bashrc
if ! grep -q "AI_STICK aliases" ~/.bashrc; then
    cat >> ~/.bashrc <<'EOFBASH'

# AI_STICK aliases
alias status='~/pi_status.sh'
alias aichat='~/ai_chat.sh'
alias stick='cd /media/ai_stick'
alias wiki='firefox http://localhost:8080 &'
EOFBASH
fi

echo "✅ Helper scripts created"
echo "   status - Check system status"
echo "   aichat - Start AI chat"
echo "   stick  - Go to AI_STICK directory"

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                  ✅ SETUP COMPLETE!                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "🎉 Your Raspberry Pi 5 is now an AI server!"
echo ""
echo "📝 IMPORTANT INFORMATION:"
echo ""
echo "🔗 Tailscale IP: $(tailscale ip -4)"
echo "   Use this IP to connect from your iPhone via Terminus"
echo ""
echo "📱 FROM YOUR IPHONE (Terminus app):"
echo "   Host: $(tailscale ip -4)"
echo "   Port: 22"
echo "   User: pi"
echo ""
echo "💻 QUICK COMMANDS:"
echo "   status          - Check all services"
echo "   aichat          - Chat with AI"
echo "   ollama list     - See installed models"
echo ""
echo "🌐 ACCESS WIKIPEDIA:"
echo "   Open Safari to: http://$(tailscale ip -4):8080"
echo ""
echo "📚 KNOWLEDGE AVAILABLE:"
du -sh /media/ai_stick/knowledge/* 2>/dev/null | head -5
echo ""
echo "🔄 Services auto-start on boot"
echo "🚀 Reboot recommended: sudo reboot"
echo ""
