#!/bin/bash
# Download Windows Rescue Tools

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         DOWNLOADING WINDOWS RESCUE TOOLS                  ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo

# Determine if we're on Mac or Pi
if [[ "$OSTYPE" == "darwin"* ]]; then
    BOOT_DIR="/Volumes/AI_STICK/boot"
else
    BOOT_DIR="/media/pi/AI_STICK/boot"
fi

mkdir -p "$BOOT_DIR"
cd "$BOOT_DIR" || exit 1

echo "📥 Download location: $BOOT_DIR"
echo

# SystemRescue - The best for Windows repair
echo "1️⃣  SystemRescue Linux (Best for Windows repair)"
echo "   Size: ~700MB"
echo "   Features: Windows ntfs tools, boot repair, data recovery"
echo
read -p "   Download SystemRescue? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "   🔽 Downloading SystemRescue..."
    wget -O systemrescue.iso "https://sourceforge.net/projects/systemrescuecd/files/latest/download" || {
        echo "   ❌ Download failed. Try manually:"
        echo "      https://www.system-rescue.org/Download/"
    }
fi
echo

# Clonezilla - Data backup
echo "2️⃣  Clonezilla (Disk imaging and backup)"
echo "   Size: ~350MB"
echo "   Features: Full disk backup, partition cloning"
echo
read -p "   Download Clonezilla? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "   🔽 Downloading Clonezilla..."
    # Get latest version
    wget -O clonezilla.iso "https://sourceforge.net/projects/clonezilla/files/latest/download" || {
        echo "   ❌ Download failed. Try manually:"
        echo "      https://clonezilla.org/downloads.php"
    }
fi
echo

# GParted Live - Partition management
echo "3️⃣  GParted Live (Partition editor)"
echo "   Size: ~400MB"
echo "   Features: Resize, repair, manage partitions"
echo
read -p "   Download GParted? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "   🔽 Downloading GParted..."
    wget -O gparted.iso "https://sourceforge.net/projects/gparted/files/latest/download" || {
        echo "   ❌ Download failed. Try manually:"
        echo "      https://gparted.org/download.php"
    }
fi
echo

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                    DOWNLOAD COMPLETE                       ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo
echo "✅ ISOs saved to: $BOOT_DIR"
echo
echo "🔥 NEXT STEPS:"
echo "1. Safely eject AI_STICK"
echo "2. Plug into broken HP laptop"
echo "3. Boot from USB (press F9 at startup)"
echo "4. Select SystemRescue from Ventoy menu"
echo "5. Follow HP_LAPTOP_RESCUE_GUIDE.md"
echo
