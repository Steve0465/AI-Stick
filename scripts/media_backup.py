#!/usr/bin/env python3
"""
Media Backup - Copy photos, videos, music from Mac to AI_STICK

Backs up:
- Photos from Pictures folder (not the Photos library - that's complex)
- Videos from Movies folder
- Music from Music folder
- Screenshots from Desktop
- Downloads media files
- Voice Memos
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import hashlib

STICK = Path("/Volumes/AI_STICK")
MEDIA_BACKUP = STICK / "media/backups"
HOME = Path.home()

# What to backup
SOURCES = {
    "pictures": HOME / "Pictures",
    "movies": HOME / "Movies", 
    "music": HOME / "Music",
    "desktop": HOME / "Desktop",
    "downloads": HOME / "Downloads",
    "voice_memos": HOME / "Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings",
}

# Media extensions to grab
MEDIA_EXTENSIONS = {
    # Images
    '.jpg', '.jpeg', '.png', '.gif', '.heic', '.heif', '.raw', '.cr2', '.nef', '.tiff', '.bmp', '.webp',
    # Videos
    '.mp4', '.mov', '.avi', '.mkv', '.m4v', '.wmv', '.flv', '.webm', '.3gp',
    # Audio
    '.mp3', '.m4a', '.wav', '.aac', '.flac', '.ogg', '.wma', '.aiff',
    # Screenshots
    '.png',
}

# Skip these folders
SKIP_FOLDERS = {
    '.Trash', 'node_modules', '.git', '__pycache__', 'venv', '.venv',
    'Library', 'Applications', '.npm', '.cache'
}


def get_file_hash(filepath, chunk_size=8192):
    """Quick hash for duplicate detection (first 8KB only for speed)."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(chunk_size)
            hasher.update(chunk)
    except:
        return None
    return hasher.hexdigest()[:16]


def human_size(size_bytes):
    """Convert bytes to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f}TB"


def scan_media(source_path, category):
    """Find all media files in a directory."""
    files = []
    
    if not source_path.exists():
        return files
    
    for root, dirs, filenames in os.walk(source_path):
        # Skip unwanted directories
        dirs[:] = [d for d in dirs if d not in SKIP_FOLDERS and not d.startswith('.')]
        
        for filename in filenames:
            if filename.startswith('.'):
                continue
            
            ext = Path(filename).suffix.lower()
            if ext in MEDIA_EXTENSIONS:
                filepath = Path(root) / filename
                try:
                    size = filepath.stat().st_size
                    mtime = filepath.stat().st_mtime
                    files.append({
                        "path": filepath,
                        "name": filename,
                        "size": size,
                        "mtime": mtime,
                        "category": category,
                        "ext": ext,
                    })
                except:
                    pass
    
    return files


def backup_media(files, dest_base, dry_run=False):
    """Copy media files to stick."""
    copied = 0
    skipped = 0
    total_size = 0
    seen_hashes = set()
    
    for f in files:
        # Create category folder
        dest_folder = dest_base / f["category"]
        dest_folder.mkdir(parents=True, exist_ok=True)
        
        dest_path = dest_folder / f["name"]
        
        # Handle duplicates by name
        if dest_path.exists():
            # Check if same file
            if dest_path.stat().st_size == f["size"]:
                skipped += 1
                continue
            # Different file, rename
            stem = dest_path.stem
            suffix = dest_path.suffix
            counter = 1
            while dest_path.exists():
                dest_path = dest_folder / f"{stem}_{counter}{suffix}"
                counter += 1
        
        # Check for content duplicates
        file_hash = get_file_hash(f["path"])
        if file_hash and file_hash in seen_hashes:
            skipped += 1
            continue
        if file_hash:
            seen_hashes.add(file_hash)
        
        # Copy
        if not dry_run:
            try:
                shutil.copy2(f["path"], dest_path)
                copied += 1
                total_size += f["size"]
                print(f"   📄 {f['category']}/{f['name']} ({human_size(f['size'])})")
            except Exception as e:
                print(f"   ❌ Failed: {f['name']} - {e}")
        else:
            copied += 1
            total_size += f["size"]
    
    return copied, skipped, total_size


def main():
    print("=" * 60)
    print("📸 MEDIA BACKUP - Copy your stuff to AI_STICK")
    print("=" * 60)
    
    # Check stick
    if not STICK.exists():
        print("❌ AI_STICK not mounted!")
        return
    
    # Check free space
    stat = os.statvfs(STICK)
    free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
    print(f"💾 AI_STICK free space: {free_gb:.1f}GB")
    
    # Create backup folder with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = MEDIA_BACKUP / timestamp
    
    print("\n🔍 Scanning for media files...")
    
    all_files = []
    for category, source in SOURCES.items():
        files = scan_media(source, category)
        if files:
            total_size = sum(f["size"] for f in files)
            print(f"   {category}: {len(files)} files ({human_size(total_size)})")
            all_files.extend(files)
    
    if not all_files:
        print("\n❌ No media files found!")
        return
    
    total_size = sum(f["size"] for f in all_files)
    print(f"\n📊 Total: {len(all_files)} files ({human_size(total_size)})")
    
    # Check if it fits
    if total_size / (1024**3) > free_gb * 0.9:
        print(f"⚠️ Warning: May not have enough space!")
    
    # Confirm
    print("\nOptions:")
    print("  1) Full backup (copy everything)")
    print("  2) New only (skip if already backed up)")
    print("  3) Dry run (show what would be copied)")
    print("  0) Cancel")
    
    choice = input("\nSelect option: ").strip()
    
    if choice == "0":
        print("Cancelled.")
        return
    
    dry_run = (choice == "3")
    
    # For "new only", check existing backups
    if choice == "2":
        # Use latest backup folder if exists
        existing = sorted(MEDIA_BACKUP.glob("*")) if MEDIA_BACKUP.exists() else []
        if existing:
            backup_folder = existing[-1]
            print(f"📁 Adding to existing backup: {backup_folder.name}")
    
    print(f"\n{'🔍 DRY RUN - ' if dry_run else ''}Starting backup...")
    
    copied, skipped, size = backup_media(all_files, backup_folder, dry_run=dry_run)
    
    print("\n" + "=" * 60)
    print(f"✅ {'Would copy' if dry_run else 'Copied'}: {copied} files ({human_size(size)})")
    print(f"⏭️ Skipped (duplicates): {skipped}")
    if not dry_run:
        print(f"📁 Location: {backup_folder}")
    print("=" * 60)


if __name__ == "__main__":
    main()
