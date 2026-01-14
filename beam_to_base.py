import os
import shutil
import json
import time
import requests
from tqdm import tqdm

# --- CONFIGURATION ---
STICK_ROOT = os.path.dirname(os.path.abspath(__file__))
TRANSFER_ZONE = os.path.join(STICK_ROOT, '_transfer_zone')
SENT_ZONE = os.path.join(TRANSFER_ZONE, 'sent')
CONFIG_FILE = os.path.join(STICK_ROOT, 'beam_config.json')

# Ensure directories exist
os.makedirs(SENT_ZONE, exist_ok=True)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def main():
    print("--- BEAM TO BASE (Tailscale Upload) ---")
    
    config = load_config()
    
    # Get IP Address
    base_ip = config.get('base_ip')
    if not base_ip:
        base_ip = input("Enter Godman Command Center IP (Tailscale): ").strip()
        config['base_ip'] = base_ip
        save_config(config)
    else:
        print(f"Target Base: {base_ip}")

    # Get Access Key
    access_key = config.get('access_key')
    if not access_key:
        access_key = input("Enter Access Key: ").strip()
        config['access_key'] = access_key
        save_config(config)
    
    api_url = f"http://{base_ip}:8080/api/upload"

    # Scan for files
    files_to_send = []
    print(f"\nScanning {TRANSFER_ZONE}...")
    
    for root, dirs, files in os.walk(TRANSFER_ZONE):
        if 'sent' in root: # Skip the sent folder
            continue
            
        for file in files:
            if file.startswith('.'): continue # Skip hidden
            files_to_send.append(os.path.join(root, file))

    if not files_to_send:
        print("No files found to beam up.")
        input("Press Enter to exit...")
        return

    print(f"Found {len(files_to_send)} files.")
    confirm = input("Start upload? (y/n): ").lower()
    if confirm != 'y':
        return

    # Upload Loop
    success_count = 0
    
    for file_path in tqdm(files_to_send, unit="file"):
        filename = os.path.basename(file_path)
        
        try:
            with open(file_path, 'rb') as f:
                response = requests.post(
                    api_url,
                    files={'file': f},
                    headers={'x-access-key': access_key},
                    timeout=30
                )
            
            if response.status_code == 200:
                # Move to sent folder
                dest_path = os.path.join(SENT_ZONE, filename)
                # Handle name collision in sent folder
                counter = 1
                base, ext = os.path.splitext(filename)
                while os.path.exists(dest_path):
                    dest_path = os.path.join(SENT_ZONE, f"{base}_{counter}{ext}")
                    counter += 1
                
                shutil.move(file_path, dest_path)
                success_count += 1
            else:
                tqdm.write(f"Failed to upload {filename}: {response.status_code} - {response.text}")

        except Exception as e:
            tqdm.write(f"Error uploading {filename}: {e}")

    print(f"\nOperation Complete. {success_count}/{len(files_to_send)} files beamed.")
    if os.name == 'nt':
        os.system("pause")
    else:
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
