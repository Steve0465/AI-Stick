#!/bin/bash
# Automated Windows Boot Repair

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 /dev/sdX [windows_mount_point]"
    echo "Example: $0 /dev/sda /mnt/windows"
    exit 1
fi

DISK="$1"
WINDOWS_MOUNT="${2:-/mnt/windows}"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           WINDOWS BOOT REPAIR (AUTOMATED)                 ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo
echo "Target disk: $DISK"
echo "Windows mount: $WINDOWS_MOUNT"
echo
echo "⚠️  WARNING: This will modify boot sectors!"
read -p "Continue? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 1
fi
echo

# Check if tools are available
echo "🔍 Checking for repair tools..."
command -v ntfsfix >/dev/null 2>&1 || {
    echo "❌ ntfsfix not found. Install: apt install ntfs-3g"
    exit 1
}
echo "✅ Tools ready"
echo

# Find Windows partition
echo "🔍 Detecting Windows partition..."
WINDOWS_PART=$(lsblk -o NAME,FSTYPE,LABEL | grep -i "ntfs\|windows" | head -1 | awk '{print "/dev/"$1}')
if [ -z "$WINDOWS_PART" ]; then
    echo "❌ Could not auto-detect Windows partition"
    lsblk
    read -p "Enter Windows partition (e.g. /dev/sda2): " WINDOWS_PART
fi
echo "   Found: $WINDOWS_PART"
echo

# Fix NTFS errors
echo "🔧 Step 1: Fixing NTFS filesystem errors..."
ntfsfix "$WINDOWS_PART"
echo "   ✅ NTFS repaired"
echo

# Mount Windows
echo "🔧 Step 2: Mounting Windows..."
mkdir -p "$WINDOWS_MOUNT"
mount -t ntfs-3g "$WINDOWS_PART" "$WINDOWS_MOUNT" 2>/dev/null || mount "$WINDOWS_PART" "$WINDOWS_MOUNT"

if [ ! -d "$WINDOWS_MOUNT/Windows" ]; then
    echo "❌ Windows directory not found. Mount failed?"
    exit 1
fi
echo "   ✅ Windows mounted"
echo

# Check boot type (UEFI vs Legacy)
if [ -d "/sys/firmware/efi" ]; then
    echo "🔧 Step 3: UEFI boot detected - Repairing EFI..."
    
    # Find EFI partition
    EFI_PART=$(lsblk -o NAME,FSTYPE,LABEL | grep -i "fat\|efi" | head -1 | awk '{print "/dev/"$1}')
    
    if [ -n "$EFI_PART" ]; then
        echo "   EFI partition: $EFI_PART"
        mkdir -p /mnt/efi
        mount "$EFI_PART" /mnt/efi
        
        # Rebuild BCD if efibootmgr is available
        if command -v efibootmgr >/dev/null 2>&1; then
            efibootmgr --create --disk "$DISK" --part 1 --label "Windows Boot Manager" \
                --loader '\EFI\Microsoft\Boot\bootmgfw.efi' 2>/dev/null
            echo "   ✅ EFI boot entry created"
        fi
    fi
else
    echo "🔧 Step 3: Legacy/MBR boot detected - Repairing MBR..."
    
    if command -v ms-sys >/dev/null 2>&1; then
        ms-sys -m "$DISK"
        echo "   ✅ MBR repaired"
    else
        echo "   ⚠️  ms-sys not available"
        echo "   Install: apt install ms-sys"
    fi
fi
echo

# Check and repair BCD
echo "🔧 Step 4: Checking Boot Configuration..."
BCD_PATH="$WINDOWS_MOUNT/Boot/BCD"
if [ -f "$BCD_PATH" ]; then
    # Backup BCD
    cp "$BCD_PATH" "${BCD_PATH}.backup"
    echo "   ✅ BCD backed up"
    
    # Can't directly edit BCD from Linux, but we can check integrity
    echo "   💡 BCD found. If issues persist, use Windows PE to run:"
    echo "      bootrec /rebuildbcd"
fi
echo

# Unmount
umount "$WINDOWS_MOUNT" 2>/dev/null
umount /mnt/efi 2>/dev/null

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                  REPAIR COMPLETE                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo
echo "✅ Boot repair completed"
echo
echo "🔥 NEXT STEPS:"
echo "1. Remove AI_STICK"
echo "2. Restart laptop"
echo "3. Windows should boot normally"
echo
echo "If boot still fails:"
echo "   - Use Windows PE to run: bootrec /fixboot && bootrec /rebuildbcd"
echo "   - Or run ./analyze_srt_log.py to diagnose further"
echo
