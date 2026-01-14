#!/bin/bash
# Backup Windows User Data

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 /path/to/windows/mount /path/to/backup/destination"
    echo "Example: $0 /mnt/windows /media/usb/backup"
    exit 1
fi

WINDOWS_MOUNT="$1"
BACKUP_DEST="$2"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║             WINDOWS USER DATA BACKUP                       ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo
echo "Source: $WINDOWS_MOUNT"
echo "Destination: $BACKUP_DEST"
echo

mkdir -p "$BACKUP_DEST"

# Find user directories
USERS_DIR="$WINDOWS_MOUNT/Users"

if [ ! -d "$USERS_DIR" ]; then
    echo "❌ Windows Users directory not found at: $USERS_DIR"
    exit 1
fi

echo "🔍 Found users:"
ls -1 "$USERS_DIR" | grep -v "Public\|Default\|All Users"
echo

# Backup each user
for user_dir in "$USERS_DIR"/*; do
    username=$(basename "$user_dir")
    
    # Skip system directories
    if [[ "$username" == "Public" || "$username" == "Default" || "$username" == "All Users" ]]; then
        continue
    fi
    
    echo "📦 Backing up: $username"
    
    # Create user backup directory
    user_backup="$BACKUP_DEST/$username"
    mkdir -p "$user_backup"
    
    # Backup important directories
    for folder in Desktop Documents Downloads Pictures Videos Music; do
        source_path="$user_dir/$folder"
        if [ -d "$source_path" ]; then
            echo "   📁 $folder..."
            rsync -ah --info=progress2 "$source_path" "$user_backup/" 2>/dev/null || {
                cp -r "$source_path" "$user_backup/" 2>/dev/null
            }
        fi
    done
    
    # Backup browser data
    echo "   🌐 Browser bookmarks..."
    # Chrome
    [ -d "$user_dir/AppData/Local/Google/Chrome/User Data" ] && \
        mkdir -p "$user_backup/Chrome" && \
        cp -r "$user_dir/AppData/Local/Google/Chrome/User Data/Default/Bookmarks" "$user_backup/Chrome/" 2>/dev/null
    
    # Firefox
    [ -d "$user_dir/AppData/Roaming/Mozilla/Firefox" ] && \
        mkdir -p "$user_backup/Firefox" && \
        cp -r "$user_dir/AppData/Roaming/Mozilla/Firefox" "$user_backup/Firefox/" 2>/dev/null
    
    echo "   ✅ $username backup complete"
    echo
done

# Calculate backup size
BACKUP_SIZE=$(du -sh "$BACKUP_DEST" | cut -f1)

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                  BACKUP COMPLETE                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo
echo "✅ Backup location: $BACKUP_DEST"
echo "📊 Total size: $BACKUP_SIZE"
echo
echo "💡 Files backed up:"
echo "   - Desktop"
echo "   - Documents"
echo "   - Downloads"
echo "   - Pictures"
echo "   - Videos"
echo "   - Music"
echo "   - Browser bookmarks"
echo
