import os
import shutil
import time
import subprocess

# --- CONFIG ---
STICK_ROOT = os.path.dirname(os.path.abspath(__file__))
DEST_BASE = os.path.join(STICK_ROOT, '_transfer_zone', 'Phone_Drops')
MEDIA_EXTS = {'.jpg', '.jpeg', '.png', '.heic', '.mp4', '.mov', '.avi'}

# Common mount points on Linux/Pi for MTP/Phones
MTP_PATHS = [
    f"/run/user/{os.getuid()}/gvfs/", 
    "/media/pi/"
]

def find_phone():
    """Scans common mount points for a phone or camera DCIM folder."""
    for base in MTP_PATHS:
        if not os.path.exists(base): continue
        for root, dirs, files in os.walk(base):
            if 'DCIM' in dirs:
                return os.path.join(root, 'DCIM')
    return None

def main():
    print("📱 --- PHONE DROP: UNIVERSAL SIPHON ---")
    print("Waiting for phone connection...")
    print("(Make sure to select 'File Transfer' or 'Allow Access' on your phone)")
    
    while True:
        phone_path = find_phone()
        
        if phone_path:
            print(f"✨ Phone Detected at: {phone_path}")
            stamp = time.strftime('%Y-%m-%d_%H%M')
            dest_folder = os.path.join(DEST_BASE, f"Drop_{stamp}")
            os.makedirs(dest_folder, exist_ok=True)
            
            print(f"📥 Siphoning media to: {dest_folder}...")
            
            count = 0
            for root, dirs, files in os.walk(phone_path):
                for f in files:
                    if any(f.lower().endswith(ext) for ext in MEDIA_EXTS):
                        try:
                            # Avoid copying thumbnails or small cache files
                            src_file = os.path.join(root, f)
                            if os.path.getsize(src_file) > 50000: # > 50KB
                                shutil.copy2(src_file, os.path.join(dest_folder, f))
                                count += 1
                                if count % 10 == 0:
                                    print(f"   Pulled {count} files...", end='\r')
                        except: pass
            
            print(f"\n✅ SUCCESS! {count} files secured from phone.")
            print("You can safely unplug the phone.")
            
            # Wait for phone to be unplugged to avoid re-triggering
            while find_phone():
                time.sleep(5)
            print("\nWaiting for next device...")
            
        time.sleep(5)

if __name__ == "__main__":
    main()
