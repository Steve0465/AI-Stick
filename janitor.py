import os
import shutil
import datetime
import sys

# Configuration
EXTENSIONS = {'.pdf', '.csv', '.xlsx', '.jpg', '.png'}
# Determine where we are running from (the stick)
STICK_ROOT = os.path.dirname(os.path.abspath(__file__))
TRANSFER_ZONE = os.path.join(STICK_ROOT, '_transfer_zone')

def get_user_folder(folder_name):
    """Returns the path to the user's Desktop or Downloads folder."""
    home = os.path.expanduser("~")
    return os.path.join(home, folder_name)

def log_manifest(destination_folder, copied_files):
    """Writes a log of transferred files."""
    manifest_path = os.path.join(destination_folder, 'manifest.txt')
    try:
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(f"Scan Date: {datetime.datetime.now()}\n")
            f.write(f"Total Files: {len(copied_files)}\n")
            f.write("-" * 40 + "\n")
            for src, dest in copied_files:
                f.write(f"Source: {src}\nDest:   {dest}\n\n")
    except Exception as e:
        print(f"Warning: Could not write manifest file: {e}")

def main():
    print("--- Digital Janitor (AI Stick) ---")
    print(f"Storage Root: {STICK_ROOT}")
    print("1. Scan Desktop")
    print("2. Scan Downloads")
    
    choice = input("Select target (1 or 2): ").strip()

    if choice == '1':
        target_dir = get_user_folder('Desktop')
    elif choice == '2':
        target_dir = get_user_folder('Downloads')
    else:
        print("Invalid choice. Exiting.")
        return

    if not os.path.exists(target_dir):
        print(f"Directory not found: {target_dir}")
        return

    # Create timestamped folder
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    dest_dir = os.path.join(TRANSFER_ZONE, f"{timestamp}_Import")
    
    try:
        os.makedirs(dest_dir, exist_ok=True)
    except OSError as e:
        print(f"Error creating destination directory {dest_dir}: {e}")
        return

    print(f"Scanning {target_dir} for {EXTENSIONS}...")
    copied_files = []

    # Walk the directory
    for root, dirs, files in os.walk(target_dir):
        # Skip hidden directories (like .DS_Store container folders, .git, etc.)
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            # Skip hidden files
            if file.startswith('.'):
                continue
                
            _, ext = os.path.splitext(file)
            if ext.lower() in EXTENSIONS:
                src_path = os.path.join(root, file)
                
                # Simple flatten strategy: Copy to root of import folder
                # Handle name collisions by appending counter
                dest_path = os.path.join(dest_dir, file)
                counter = 1
                base_name = os.path.splitext(file)[0]
                
                while os.path.exists(dest_path):
                    dest_path = os.path.join(dest_dir, f"{base_name}_{counter}{ext}")
                    counter += 1

                try:
                    shutil.copy2(src_path, dest_path)
                    print(f"Copied: {file}")
                    copied_files.append((src_path, dest_path))
                except Exception as e:
                    print(f"Error copying {file}: {e}")

    log_manifest(dest_dir, copied_files)
    print(f"\nOperation complete.")
    print(f"Files moved: {len(copied_files)}")
    print(f"Location: {dest_dir}")
    # Pause so user can see output on Windows
    if os.name == 'nt':
        os.system("pause")
    else:
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
